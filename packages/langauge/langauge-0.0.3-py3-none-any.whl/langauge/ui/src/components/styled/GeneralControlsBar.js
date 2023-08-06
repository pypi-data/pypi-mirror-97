// Copyright (c) FlapMX LLC.
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.

import styled from "styled-components";

export const GeneralControlsBar = styled.div`
  padding: 10px 10px 0 0;
  display: flex;
  flex-flow: row nowrap;
  justify-content: flex-end;
  align-items: center;

  button {
    margin: 0 10px;
  }

  .upload-container input {
    display: none;
  }
`;
