"""File upload and service."""

import os

from uuid import UUID, uuid4
from cgi import FieldStorage

from zoom import Page, Record, system as context, store, redirect_to, \
    html, authorize, dispatch, load as load_app_asset, requires as requires_lib
from zoom.mvc import View
from zoom.render import render as render_template
from zoom.helpers import abs_url_for
from zoom.buckets import FileBucket
from zoom.response import Response
from zoom.logging import log_activity

# Define constants.
ICON_NAMES = (
    (('png', 'jpg', 'jpeg', 'tiff', 'svg'), 'fa-file-image-o'),
    (('pdf',), 'fa-file-pdf-o'),
    (('html', 'javascript', 'css', 'json'), 'fa-file-code-o'),
    (('zip', 'tar'), 'fa-file-archive-o'),
    (('mp3', 'aiff', 'ogg', 'wav'), 'fa-file-audio-o'),
    (('mp4', 'flv', 'wmv'), 'fa-file-video-o'),
    (('text', 'txt'), 'fa-file-text-o')
)
VIEW_IN_BROWSER = ('png', 'jpg', 'jpeg', 'tiff', 'svg', 'pdf')
EDIT_FOOTER = """
    <div class="field_edit">
        <a class="button" href="/content/files">Done</a>
    </div>
"""

# Define helpers.
def get_bucket():
    """Return a bucket for file storage."""
    return FileBucket(os.path.join(context.site.data_path, 'buckets'))

def icon_name_for(mimetype):
    """Return the FontAwesome icon name for the given mime-type."""
    for entry in ICON_NAMES:
        types, icon = entry
        for typ in types:
            if typ in mimetype:
                return icon

    return 'fa-file-o'

def get_markdown_linker(access_url, link_name, classed=None):
    """Return the markup for a markdown linker that corresponds to the logic in
    markdown-linker.js."""
    return html.tag(
        'i',
        str(),
        classed='fa fa-link markdown-linker %s'%(classed or str()),
        title='Copy markdown link',
        **{
            'data-link': abs_url_for(access_url),
            'data-link-name': link_name
        }
    )

def render_fileset_view(edit=False, **page_kwargs):
    """Serve the view for the file set, with edit mode on or off."""
    # Load and de-template the page.
    template = load_app_asset('views/file-manager.html')
    content = render_template(
        template,
        file_list=''.join(list(
            stored_file.render_view(edit=edit) for stored_file \
                    in StoredFile.collection()
        )),
        mode='edit' if edit else 'view',
        footer=EDIT_FOOTER if edit else str()
    )

    # Add the library dependency of Font Awesome and respond.
    requires_lib('fontawesome4')
    return Page(
        content, title='Files',
        styles=('/content/static/file-manager.css',),
        libs=(
            '/content/static/file-manager.js',
            '/content/static/markdown-linker.js'
        ),
        **page_kwargs
    )

# Define the record.
class StoredFile(Record):
    """A stored file."""

    @classmethod
    def collection(cls):
        return store.store_of(cls)

    @property
    def access_url(self):
        return '/content/files/' + self.id

    @property
    def access_link(self):
        return html.tag('a', self.filename, href=self.access_url)

    @property
    def filename(self):
        return self.original_name or '[no name]'

    def render_view(self, edit=False):
        """Render and return the view for this stored file, optionally with
        edit options."""
        return html.tag(
            'div',
            ''.join((
                html.tag(
                    'a',
                    ''.join((
                        html.tag('i', classed='fa ' + icon_name_for(
                            self.mimetype
                        )),
                        self.filename
                    )),
                    href=self.access_url,
                    target='_blank',
                    title='Click to view',
                ),
                get_markdown_linker(
                    self.access_url, self.filename, '--fm-link-host'
                ),
                str() if not edit else html.tag(
                    'div',
                    html.tag(
                        'div',
                        '(delete)',
                        classed='--fm-delete',
                        id=self.id,
                        role='button'
                    ),
                    classed='--fm-file-controls'
                )
            )),
            classed='--fm-file-item'
        )

# Define MVC components.
class FileSetView(View):
    """The file set view."""

    @authorize('managers')
    def index(self, *route, **req_data):
        return render_fileset_view(edit=False, actions=('Edit',))

    @authorize('managers')
    def edit(self, *route, **req_data):
        if route and route[-1] == 'done':
            return redirect_to('/content/files')

        return render_fileset_view(edit=True)

    def show(self, *route, **req_data):
        """Serves the file with the ID given as the tail of the request path."""
        # This holds the file reference we tried to serve.
        attempted_file = None

        # Define a 404 generation helper.
        def no_file():
            """Return a 404 indicating the requested file DNE."""
            return Response(
                content=bytes(
                    '%s not found'%(attempted_file or '<nothing>'), 'utf-8'
                ),
                status='404 Not Found'
            )

        # Assert the route contains a tail.
        if len(route) != 1:
            return no_file()
        # Assert the tail is a valid UUID.
        attempted_file = route[0]
        query = dict()
        try:
            query['id'] = UUID(attempted_file).hex
        except ValueError:
            query['original_name'] = attempted_file
        # Retrieve the file with the given ID and assert it exists.
        to_view = StoredFile.collection().first(**query)
        if not to_view:
            return no_file()

        # Decide whether or not to download.
        should_download = False
        if 'download' in req_data:
            should_download = True
        else:
            should_download = True

            for typ in VIEW_IN_BROWSER:
                if not should_download:
                    continue
                if typ in to_view.mimetype:
                    should_download = False

        # Serve the file.
        disposition = 'attachment' if should_download else 'inline'
        bucket = get_bucket()
        return Response(
            bucket.get(to_view.data_id),
            headers={
                'Content-Type': to_view.mimetype,
                'Content-Disposition': '%s; filename=%s'%(
                    disposition, to_view.filename
                )
            }
        )

class FileSetController(View):
    """The file set controller."""

    @authorize('managers')
    def delete(self, *route, **req_data):
        """Handle a file delete."""
        # Read the file ID from the request, with safety.
        try:
            file_id = UUID(req_data['file_id']).hex
        except ValueError:
            return Response(status='400 Bad Request')

        # Retrieve and delete the file.
        stored_files = StoredFile.collection()
        to_delete = stored_files.first(id=file_id)

        log_activity('%s deleted file %s'%(
            context.user.link, to_delete.filename
        ))

        stored_files.delete(to_delete)
        get_bucket().delete(to_delete.data_id)

        return Response(status='200 OK')

    @authorize('managers')
    def upload(self, *route, **req_data):
        """Handle a file upload."""
        # Read the FieldStorage.
        file_desc = req_data['file']
        file_mimetype = req_data['mimetype']
        if not isinstance(file_desc, FieldStorage):
            # Python is dangerous when the type is incorrectly assumed.
            return Response(b'invalid request body', status='400 Bad Request')

        # Persist the file.
        data_id = get_bucket().put(file_desc.value)
        to_store = StoredFile(
            id=uuid4().hex,
            data_id=data_id,
            mimetype=file_mimetype,
            content_length=len(file_desc.value),
            original_name=file_desc.filename
        )
        StoredFile.collection().put(to_store)

        log_activity('%s uploaded file %s'%(
            context.user.link, to_store.access_link
        ))

        # Respond.
        return Response(
            bytes(to_store.access_url, 'utf-8'),
            status='201 Created'
        )

# Define main.
main = dispatch(FileSetController, FileSetView)
