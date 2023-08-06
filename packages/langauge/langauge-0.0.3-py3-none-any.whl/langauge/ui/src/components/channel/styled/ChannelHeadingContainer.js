// Copyright (c) FlapMX LLC.
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.

import styled from "styled-components";

export const ChannelHeadingContainer = styled.div`
  font-family: "Nunito", sans-serif;
  width: 92%;
  display: grid;
  justify-content: space-between;
  justify-items: center;
  align-items: center;
  grid-template-columns: 5% 10% 15% 15% 45%;
  grid-template-rows: 75px;

  @media (max-width: 1275px) {
    width: 100%;
  }
`;
