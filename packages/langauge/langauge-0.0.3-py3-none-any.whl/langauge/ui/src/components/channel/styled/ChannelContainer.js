// Copyright (c) FlapMX LLC.
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.

import styled from "styled-components";

export const ChannelContainer = styled.div`
  border-top: 1px solid #bdbdbd;
  transition: 0.2s opacity ease-in;
`;

export const ChannelContainerInner = styled.div`
  font-family: "Lora", serif;
  width: 92%;
  display: grid;
  justify-content: space-between;
  justify-items: center;

  align-items: center;
  grid-template-columns: 5% 10% 15% 15% 45%;
  grid-template-rows: 250px;

  .fill-block {
    width: 50px;
  }

  .channel-title-span {
    font-size: 1.5rem;
  }

  .fas {
    cursor: pointer;
  }

  .fa-trash-alt:hover {
    color: #f2f2f2;
  }

  .channel-title-and-control {
    width: 100%;
    display: flex;
    justify-content: space-evenly;
    align-items: center;

    .fa-check {
      font-size: 1.2rem;
      color: green;
      margin-right: 8px;

      &:hover {
        color: #90ee90;
      }
    }

    .fa-times {
      font-size: 1.2rem;
      color: red;

      &:hover {
        color: #ffcccb;
      }
    }
  }

  @media (max-width: 1275px) {
    width: 100%;
    grid-template-rows: 300px;
  }
`;
