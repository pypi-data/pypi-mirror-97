// Copyright (c) FlapMX LLC.
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.

import React from "react";
import { Link, useRouteMatch } from "react-router-dom";
import { TabData } from "../data/TabData";

function Tab({ label, to, activeOnlyWhenExact }) {
  let match = useRouteMatch({
    path: to,
    exact: activeOnlyWhenExact,
  });

  return (
    <Link
      className={match ? "tab-list-item tab-list-active" : "tab-list-item"}
      to={to}
      style={{ textDecoration: "none" }}
    >
      {label}
    </Link>
  );
}

function Tabs() {
  return (
    <div className="tabs">
      <div className="tab-list">
        {TabData.map((item, index) => (
          <Tab
            activeOnlyWhenExact={true}
            key={index}
            to={item.path}
            label={item.title}
          />
        ))}
      </div>
    </div>
  );
}

export default Tabs;
