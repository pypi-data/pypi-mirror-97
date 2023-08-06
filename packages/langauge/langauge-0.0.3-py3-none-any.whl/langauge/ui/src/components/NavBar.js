// Copyright (c) FlapMX LLC.
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.

import LanLogo from "../assets/images/lanlogo.png";
import React from "react";
import Tabs from "./Tabs";

function NavBar() {
  return (
    <nav className="navbar navbar-expand-lg fixed-top ">
      <div className="logo-header">
        <img src={LanLogo} alt="" />
        <h1>
          Lan<i style={{ marginRight: "3px" }}>G</i>auge
        </h1>
      </div>
      <div>
        <Tabs />
      </div>
      <div className="navbar-nav ml-auto">
        <div className="nav-out-links">
          <a
            target="_blank"
            rel="noopener noreferrer"
            href="http://www.docs.langauge.org/"
          >
            Docs
          </a>
          <a
            target="_blank"
            rel="noopener noreferrer"
            href="https://github.com/flapmx/LanGauge"
          >
            GitHub
          </a>
        </div>
      </div>
    </nav>
  );
}

export default NavBar;
