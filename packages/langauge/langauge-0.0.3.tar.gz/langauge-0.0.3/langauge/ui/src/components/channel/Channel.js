// Copyright (c) FlapMX LLC.
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.

import React, { useEffect, useState } from "react";
import FileUpload from "./FileUpload";
import TaskSelect from "./TaskSelect";
import ModelSelect from "./ModelSelect";
import Preview from "./Preview";
import Buttons from "./Buttons";
import {
  ChannelContainer,
  ChannelContainerInner,
} from "./styled/ChannelContainer";
import "./.main.css";

const Channel = ({
  i,
  channel,
  changeChannelState,
  removeChannel,
  isValid,
  tasks,
  onTaskChange,
  onModelChange,
  onFileChange,
  runModel,
  downloadFile,
}) => {
  const [opacity, setOpacity] = useState("0");
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    setOpacity("1");
  }, []);

  return (
    <ChannelContainer
      id={"channel-" + i}
      className="container-fluid-side row"
      style={{ opacity: opacity }}
    >
      <ChannelContainerInner>
        <div className="channel-title-and-control">
          {deleting ? (
            <div>
              <i
                onClick={() => removeChannel(channel.name)}
                className="fas fa-check"
                title="Confirm"
              ></i>
              <i
                onClick={() => setDeleting(false)}
                className="fas fa-times"
                title="Cancel"
              ></i>
            </div>
          ) : (
            <i
              onClick={() => setDeleting(true)}
              className="fas fa-trash-alt"
              title="Delete Channel"
            ></i>
          )}

          <span className="channel-title-span">{channel.name}</span>
        </div>
        <FileUpload
          formId={i}
          onFileChange={onFileChange}
          selectedFile={channel.file}
        />
        <TaskSelect
          formId={i}
          tasks={tasks}
          selectedTask={channel.task}
          onTaskChange={onTaskChange}
        />
        <ModelSelect
          formId={i}
          selectedModel={channel.model}
          models={channel.availableModels}
          onModelChange={onModelChange}
        />
        <Preview formId={i} preview={channel.preview} />
      </ChannelContainerInner>
      <Buttons
        isValid={isValid}
        changeChannelState={changeChannelState}
        formId={i}
        runModel={runModel}
        downloadFile={downloadFile}
        channel={channel}
      />
    </ChannelContainer>
  );
};

export default Channel;
