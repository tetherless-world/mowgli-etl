/* tslint:disable */
/* eslint-disable */
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: MatchingNodesQuery
// ====================================================

export interface MatchingNodesQuery_matchingNodes {
  __typename: "Node";
  aliases: string[] | null;
  datasource: string;
  id: string;
  label: string | null;
  other: string | null;
  pos: string | null;
}

export interface MatchingNodesQuery {
  matchingNodes: MatchingNodesQuery_matchingNodes[];
  matchingNodesCount: number;
}

export interface MatchingNodesQueryVariables {
  limit: number;
  offset: number;
  text: string;
  withCount: boolean;
}
