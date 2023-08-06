// Copyright (c) FlapMX LLC.
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.

import React from "react";
import { Bar, defaults } from "react-chartjs-2";

function poolColors(channelCount) {
  let colors = ["#0033FF", "#0099FF", "#0066FF", "#00CCFF"];
  let pool = [];
  for (let i = 0; i < channelCount; i++) {
    pool[i] = colors[i];
  }
  return pool;
}

function BarChart(props) {
  // Default Styles To Pass Down To Bar Children
  defaults.global.defaultFontFamily = "Nunito";
  defaults.global.defaultFontColor = "#242424";
  defaults.global.defaultFontSize = 24;

  const options = {
    legend: {
      display: true,
      align: "end",

      labels: {
        boxWidth: 0,
      },
    },
    scales: {
      yAxes: [
        {
          scaleLabel: {
            display: true,
            labelString: "Time (seconds)",
          },
          ticks: {},
        },
      ],
      xAxes: [
        {
          scaleLabel: {
            display: true,
            labelString: "Channel",
          },
          ticks: {},
        },
      ],
    },
    tooltips: {
      callbacks: {
        label: function (t, d) {
          let yLabel = d.datasets[t.datasetIndex].data[t.index];
          return yLabel.toFixed(5) + " seconds";
        },
      },
    },
  };

  let labels = props.channels.map((channel) => channel.name);

  const time_state = {
    labels: labels,
    datasets: [
      {
        label: "* Default CPU",
        backgroundColor: poolColors(Object.keys(props.data).length),
        data: Object.values(props.data),
      },
    ],
  };

  return (
    <div>
      <div className="chart-container">
        <div className="bar-div">
          <h2>Execution Time</h2>
          <Bar data={time_state} options={options} height={200} />
        </div>
      </div>
      {/*<div className="container-fluid-side row custom-row">*/}
      {/*    <Bar data={acc_state} options={options}/>*/}
      {/*</div>*/}
    </div>
  );
}

export default BarChart;
