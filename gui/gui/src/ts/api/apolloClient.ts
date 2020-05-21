import {
  InMemoryCache,
  IntrospectionFragmentMatcher,
} from "apollo-cache-inmemory";

import * as introspectionQueryResultData from "./graphqlFragmentTypes.json";

import ApolloClient from "apollo-boost";

const fragmentMatcher = new IntrospectionFragmentMatcher({
  introspectionQueryResultData: (introspectionQueryResultData as any).default,
});

const cache = new InMemoryCache({fragmentMatcher});

export const apolloClient = new ApolloClient({
  cache,
  uri: "/api/graphql",
});
