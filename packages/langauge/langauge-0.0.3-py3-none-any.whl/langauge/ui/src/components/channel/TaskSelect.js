// Copyright (c) FlapMX LLC.
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.

import React from "react";

function TaskSelect(props) {
  return (
    <div>
      <div id={"task-" + props.formId}>
        <select
          className="custom-select"
          value={props.selectedTask}
          onChange={(event) =>
            props.onTaskChange(props.formId, event.target.value)
          }
        >
          {props.tasks.map((task) => (
            <option key={task.value} value={task.value}>
              {task.display}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
}

export default TaskSelect;
