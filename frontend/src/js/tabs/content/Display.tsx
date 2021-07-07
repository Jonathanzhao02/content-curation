//Importing from outside the project
import React from 'react';

//Importing from other files in the project
import { ContentTable } from 'solarspell-react-lib';
import ActionPanel from './ActionPanel';
import ContentForm from './ContentForm';
import { Content, Metadata, MetadataType } from 'js/types';

type DisplayActionProps = {
  onEdit: (item: Content, vals: Partial<Content>) => void
  onDelete: (item: Content) => void
  onView: (item: Content) => void
}

type DisplayProps = {
  metadata: Record<number, Metadata[]>
  metadataTypes: MetadataType[]
  content: Content[]
  actions: DisplayActionProps
}

/**
 * Displays content in a table.
 * @param props Context and callbacks.
 * @returns A table to display all content.
 */
function Display({
  metadata,
  metadataTypes,
  content,
  actions,
}: DisplayProps): React.ReactElement {
  const [editedContent, setEditedContent] = React.useState<Content | undefined>();

  const onEdit_ = React.useCallback(
    (item: Content) => setEditedContent(item),
    [setEditedContent],
  );

  const onEditSubmit_ = React.useCallback(
    (item?: Partial<Content>) => {
      if (editedContent && item) {
        actions.onEdit(editedContent, item);
      }
      setEditedContent(undefined);
    },
    [actions.onEdit, editedContent, setEditedContent],
  );

  return (
    <>
      <ContentForm
        metadata={metadata}
        metadataTypes={metadataTypes}
        onSubmit={onEditSubmit_}
        open={!!editedContent}
        content={editedContent!}
        type={'edit'}
      />
      <ContentTable
        content={content}
        selectable
        components={{
          ActionPanel: ActionPanel,
        }}
        componentProps={{
          ActionPanel: {
            ...actions,
            onEdit: onEdit_,
          },
        }}
      />
    </>
  )
}

export type { DisplayActionProps };
export default Display;
