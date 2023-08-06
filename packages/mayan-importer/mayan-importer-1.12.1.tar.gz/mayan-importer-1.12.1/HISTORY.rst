1.12.1 (2021-02-23)
===================
- Require credentials 1.2 version.
- Fix backend SourceColumn label.

1.12 (2020-12-27)
=================
- Add database backed logging to import setups.
- Add events for tracking start and end of the import setup population and
  processing.
- Improve import setup state tracking.
- Improve tests and add event testing.

1.11 (2020-12-17)
=================
- Add API.

1.10.2 (2020-10-05)
===================
- Fix context variable typo.

1.10.1 (2020-10-05)
===================
- Revert usage of `task_upload_new_version`. Version
  processing is now done as part of the same code context
  as the import.

1.10.0 (2020-10-05)
===================
- Support disabling import setup state update to workaround
  overloaded databases.
- Keep track of the documents created from an import setup
  item.
- Use document `task_upload_new_version` to process the document version
  as a separate code context.
- Use a queryset iterator when launching the processing tasks of the import
  setup items to save memory.

1.9.0 (2020-10-04)
==================
- Add cabinet action. This action creates a cabinet structure from
  a path like value.
- Execute only enabled actions.
- Rename the modules of the test importer and import setup actions.
- Fix grammatical errors.

1.8.0 (2020-10-04)
==================
- Index the import setup item state field.
- Check the state of the import setup item before processing.

1.7.0 (2020-10-03)
==================
- Remove metadata mapping field.
- Add import setup actions. These are execute after the document is
  imported. Add an import setup action to assign a metadata value from
  a template.
- Backport the templating_tags from version 3.5.

1.6.0 (2020-09-30)
==================
- Fix "off-by-one" process size issue.
- Delete shared uploaded file after creating document to keep the
  ``shared_files`` folder size small.
- Update import setup clear, populating, and process views to work on single
  or multiple items.

1.5.0 (2020-09-25)
==================
- Add model filer to load and save models from and to CSV.

1.4.0 (2020-09-24)
==================
- Add import setup item completion event.
- Commit the import setup executed event when the execute
  method is called instead of the get get_backend_intsance.
- Add more tests.
- Rename fields and models for clarity. Item metadata field
  renamed to 'data' to avoid confusion with document metadata.
- Event, permission, and action named "Execute" is now "Process".
- Filter items by regular expressions during population and also
  during processing.
- Add team_admin_id field to the Dropbox backend to avoid an
  extra API call for each item to be imported.
- Multiple values are now cached for higher performance.
- Process and clear links are disabled for empty import setups.
- Smarter backend import error exclusion.
- Automatic backend keyword argument setup from dynamic fields.
- Support import item fields as attributes or dictionary keys.

1.3.0 (2020-09-23)
==================
- Add support to process individual items.
- Add background task support for individual items.
  Each item is now processed independently and in parallel.
- Add thousand comma separator to the progress summary column.

1.2.0 (2020-09-22)
==================
- Support Dropbox Team admin access.
- Add import setup state field.
- Add import setup item list view.
- Add import setup item delete view.

1.1.0 (2020-09-08)
==================
- Convert app into a general import app.
  Dropbox code moved into a separate importers module.

1.0.2 (2020-09-07)
==================
- Update absolute imports to self.

1.0.1 (2020-09-07)
==================
- Update absolute imports to the Credentials app.

1.0.0 (2020-09-01)
==================
- Initial release
