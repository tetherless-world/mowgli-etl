/* tslint:disable */
/* eslint-disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: NodePageQuery
// ====================================================

export interface NodePageQuery_nodeById {
  __typename: "Node";
  aliases: string[] | null;
  datasource: string;
  id: string;
  label: string | null;
  other: string | null;
  pos: string | null;
}

export interface NodePageQuery {
  nodeById: NodePageQuery_nodeById | null;
}

export interface NodePageQueryVariables {
  id: string;
}
