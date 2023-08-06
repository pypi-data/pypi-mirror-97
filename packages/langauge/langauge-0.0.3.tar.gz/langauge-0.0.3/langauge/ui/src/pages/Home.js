// Copyright (c) FlapMX LLC.
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.

import React, { Component } from "react";
import ColHeadings from "../components/channel/ColHeadings.js";
import Channel from "../components/channel/Channel.js";
import ConfigButtons from "../components/ConfigButtons";

class Home extends Component {
  render() {
    return (
      <>
        <div className="home-container">
          <ConfigButtons
            saveConfig={this.props.saveConfig}
            fetchConfig={this.props.fetchConfig}
            runAll={this.props.runAll}
          />
          <div className="channel-container">
            <ColHeadings
              addChannel={this.props.addChannel}
              removeChannel={this.props.removeChannel}
              channels={this.props.channels}
            />
            {this.props.channels.map((channel, i) => (
              <Channel
                i={i}
                key={channel.name}
                channel={channel}
                isValid={this.props.isValid}
                removeChannel={this.props.removeChannel}
                changeChannelState={this.props.changeChannelState}
                tasks={this.props.tasks}
                onTaskChange={this.props.onTaskChange}
                onModelChange={this.props.onModelChange}
                runModel={this.props.runModel}
                downloadFile={this.props.downloadFile}
                onFileChange={this.props.onFileChange}
              />
            ))}
          </div>
        </div>
      </>
    );
  }
}

export default Home;
