import * as React from "react";

import {Select, MenuItem, Paper} from "@material-ui/core";

import {useQuery} from "@apollo/react-hooks";

import {DatasourcesQuery} from "api/queries/types/DatasourcesQuery";
import * as DatasourcesQueryDocument from "api/queries/DatasourcesQuery.graphql";

export const DatasourceSelect: React.FunctionComponent<{
  value?: string[];
  onChange?: (newValues: string[]) => void;
  style?: React.CSSProperties;
}> = ({value, onChange, style}) => {
  const {data} = useQuery<DatasourcesQuery>(DatasourcesQueryDocument);
  const datasources = data?.datasources;

  const [selectedDatasources, setSelectedDatasources] = React.useState<
    string[]
  >(value || []);

  if (!datasources) return null;

  return (
    <Paper variant="outlined" square style={style} data-cy="datasourceSelect">
      <Select
        multiple
        displayEmpty
        value={selectedDatasources}
        onChange={(event: React.ChangeEvent<{value: unknown}>) => {
          const values = event.target.value as string[];
          setSelectedDatasources(values);
          if (onChange) onChange(values);
        }}
        renderValue={(selected) => (
          <span style={{marginLeft: "5px"}} data-cy="value">
            {(selected as string[]).length === 0 ? (
              <React.Fragment>All datasources</React.Fragment>
            ) : (
              (selected as string[]).join(", ")
            )}
          </span>
        )}
      >
        {datasources.map((datasource) => (
          <MenuItem
            key={datasource}
            value={datasource}
            data-cy="datasourceSelectMenuItem"
          >
            {datasource}
          </MenuItem>
        ))}
      </Select>
    </Paper>
  );
};
