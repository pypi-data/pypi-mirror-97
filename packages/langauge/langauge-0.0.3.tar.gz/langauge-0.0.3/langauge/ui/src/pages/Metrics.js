// Copyright (c) FlapMX LLC.
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.

import React, { useState, useEffect } from "react";
import BarChart from "../components/BarChart";

function Metrics(props) {
  const [times, setTimes] = useState({});

  const populateEmptyIndices = (time_obj) => {
    const newTimes = { ...time_obj };
    const keys = Object.keys(newTimes);
    const keysToNumber = keys.map((key) => parseInt(key, 10));

    const maxKey = Math.max(...keysToNumber);
    for (let i = 0; i <= maxKey; i++) {
      if (!newTimes[i]) {
        newTimes[i] = 0;
      }
    }
    return newTimes;
  };

  // Populates Empty Indices When Props Change
  useEffect(() => {
    setTimes(populateEmptyIndices(props.time_taken));
  }, [props.time_taken]);

  return <BarChart channels={props.channels} data={times} />;
}

export default Metrics;
