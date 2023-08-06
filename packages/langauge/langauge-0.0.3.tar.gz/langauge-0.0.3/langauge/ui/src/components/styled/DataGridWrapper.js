// Copyright (c) FlapMX LLC.
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.

import styled from "styled-components";

export const DataGridWrapper = styled.div`
  padding: 0 40px;
  width: 100%;
  display: flex;
  flex-flow: column nowrap;
  align-items: center;

  .button-generic {
    padding: 1px 0;
  }

  .grid-header {
    font-family: "Nunito", sans-serif;
    font-size: 1.2rem;
    padding: 20px 0;
    width: 100%;
    display: grid;
    grid-template-columns: 5% 22% 5% 22% 5% 15%;
    align-items: center;
    justify-items: flex-start;
    justify-content: space-between;
    border-bottom: 1px solid #bdbdbd;
  }

  .grid-rows-container {
    width: 100%;
    display: flex;
    flex-flow: column nowrap;

    .grid-row {
      padding: 10px 0;
      display: grid;
      grid-template-columns: 5% 22% 5% 22% 5% 15%;
      justify-items: flex-start;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid #f2f2f2;
    }
  }

  .grid-footer {
    height: 40px;
  }
`;
