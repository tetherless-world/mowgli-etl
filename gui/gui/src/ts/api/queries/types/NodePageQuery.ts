/* tslint:disable */
/* eslint-disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: NodePageQuery
// ====================================================

export interface NodePageQuery_nodeById_subjectOfEdges_objectNode {
  __typename: "Node";
  id: string;
  label: string | null;
  pos: string | null;
}

export interface NodePageQuery_nodeById_subjectOfEdges {
  __typename: "Edge";
  object: string;
  objectNode: NodePageQuery_nodeById_subjectOfEdges_objectNode | null;
  predicate: string | null;
}

export interface NodePageQuery_nodeById {
  __typename: "Node";
  aliases: string[] | null;
  datasource: string;
  id: string;
  label: string | null;
  other: string | null;
  pos: string | null;
  subjectOfEdges: NodePageQuery_nodeById_subjectOfEdges[];
}

export interface NodePageQuery {
  nodeById: NodePageQuery_nodeById | null;
}

export interface NodePageQueryVariables {
  id: string;
}
