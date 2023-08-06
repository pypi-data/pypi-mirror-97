// Copyright (c) FlapMX LLC.
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.

import React, { useState, useRef } from "react";
import { Button } from "@material-ui/core";
import { createMuiTheme, ThemeProvider } from "@material-ui/core/styles";

const theme = createMuiTheme({
  palette: {
    primary: {
      main: "#0664b2",
    },
  },
});

function FileUpload(props) {
  const fileInput = useRef(null);
  const [hasFile, setHasFile] = useState(props.selectedFile ? true : false);

  const fileChange = (e) => {
    // Grabbing last 4 chars of filename AKA the type
    const fileType = e.target.value.slice(e.target.value.length - 4);
    if (fileType === ".txt") {
      setHasFile(true);
    }
    // No characters = No file was uploaded.
    else if (fileType === "") {
      return;
    } else {
      alert("Input only accepts text files.");
    }

    // update file property under channel state
    props.onFileChange(props.formId, fileInput.current.files[0]);
  };

  const clearFile = () => {
    setHasFile(false);
    props.onFileChange(props.formId, null);
    fileInput.current.value = null;
  };

  return (
    <div>
      <input
        ref={fileInput}
        type="file"
        id={"file-" + props.formId}
        onChange={fileChange}
        name="myfile"
        accept=".txt"
        style={{ display: "none" }}
      />
      <div className="file-upload-label-container">
        <label className="file-upload-label" htmlFor={"file-" + props.formId}>
          <ThemeProvider theme={theme}>
            <Button
              variant="contained"
              component="span"
              size="small"
              color="primary"
              title={
                props.selectedFile ? props.selectedFile.name : "Select File"
              }
              theme={theme}
            >
              {hasFile
                ? `${props.selectedFile.name.slice(
                    0,
                    6
                  )}..${props.selectedFile.name.slice(
                    props.selectedFile.name.length - 3
                  )} `
                : "Select File"}
            </Button>
          </ThemeProvider>
        </label>
        {hasFile && (
          <div>
            <i
              onClick={clearFile}
              className="fas fa-trash-alt"
              title="Remove File"
            ></i>
          </div>
        )}
      </div>
    </div>
  );
}

export default FileUpload;
