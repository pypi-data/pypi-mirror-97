// Copyright (c) FlapMX LLC.
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.

import React from "react";

function Preview(props) {
  return (
    <div className="custom-preview">
      <div className="card-value text-small">
        <div className="previewDescription" id={"preview-" + props.formId}>
          <span>{props.preview}</span>
        </div>
      </div>
    </div>
  );
}

export default Preview;
