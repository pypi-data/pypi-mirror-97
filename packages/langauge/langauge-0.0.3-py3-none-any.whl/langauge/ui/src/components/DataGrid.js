// Copyright (c) FlapMX LLC.
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.

import React from "react";
import { DataGridWrapper } from "./styled/DataGridWrapper";
import { makeStyles } from "@material-ui/core/styles";
import CircularProgress from "@material-ui/core/CircularProgress";

const useStyles = makeStyles((theme) => ({
  root: {
    display: "flex",
    "& > * + *": {
      margin: theme.spacing(2),
    },
  },
}));

const DataRow = ({ row, setSelectionId, selectionId }) => {
  return (
    <div className="grid-row">
      <span>
        <input
          type="checkbox"
          readOnly
          onClick={() => setSelectionId(row.id)}
          checked={selectionId === row.id}
        />
      </span>
      <span>{row.id}</span>
      <span>{row.task}</span>
      <span>{row.model}</span>
      <span>{row.status}</span>
      <span>{row.date_done}</span>
    </div>
  );
};

const DataGrid = (props) => {
  const classes = useStyles();

  if (props.loading) {
    return (
      <div
        className={classes.root}
        style={{ margin: "0 auto", padding: "20px 0" }}
      >
        <CircularProgress />
      </div>
    );
  }

  return (
    <DataGridWrapper>
      <div className="grid-header">
        <button
          className="button-generic"
          title="Download"
          onClick={props.downloadFile}
        >
          <i className="fas fa-download" />
        </button>
        <span>ID</span>
        <span>Task</span>
        <span>Model</span>
        <span>Status</span>
        <span>Completion Time</span>
      </div>
      <div className="grid-rows-container">
        {props.rows &&
          props.rows.map((row) => (
            <DataRow
              key={row.id}
              row={row}
              setSelectionId={props.setSelectionId}
              selectionId={props.selectionId}
            />
          ))}
      </div>
      <div className="grid-footer"></div>
    </DataGridWrapper>
  );
};

export default DataGrid;
