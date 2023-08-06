// Copyright (c) FlapMX LLC.
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.

// utils
import React, { Component } from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import $ from "jquery";
import { ModelData } from "./data/ModelData";
import { TaskData } from "./data/TaskData";
import formatPreview from "./utils/formatPreview";
// components
import Metrics from "./pages/Metrics";
import History from "./pages/History";
import Home from "./pages/Home.js";
import NavBar from "./components/NavBar";
// styling
import "./pages/.main.css";
const host = process.env.REACT_APP_BASE_URL;

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      channels: [
        {
          name: "A",
          file: null,
          task: "",
          model: "",
          taskId: "",
          availableModels: [],
          preview: "",
          running: "none",
          success: false,
          error: false,
        },
        {
          name: "B",
          file: null,
          task: "",
          model: "",
          taskId: "",
          availableModels: [],
          preview: "",
          running: "none",
          success: false,
          error: false,
        },
      ],
      availableTasks: [],
      time_taken: {},
    };
    this.addChannel = this.addChannel.bind(this);
    this.removeChannel = this.removeChannel.bind(this);
    this.handleTimeTakenChange = this.handleTimeTakenChange.bind(this);
    this.onTaskChange = this.onTaskChange.bind(this);
    this.onModelChange = this.onModelChange.bind(this);
    this.onFileChange = this.onFileChange.bind(this);
    this.changeChannelState = this.changeChannelState.bind(this);

    this.runAll = this.runAll.bind(this);
    this.saveConfig = this.saveConfig.bind(this);
    this.fetchConfig = this.fetchConfig.bind(this);
    this.downloadFile = this.downloadFile.bind(this);
    this.update_preview = this.update_preview.bind(this);
    this.update_run = this.update_run.bind(this);
    this.runModel = this.runModel.bind(this);
    this.isValid = this.isValid.bind(this);
  }

  componentDidMount() {
    fetch(host + "/config/task")
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        let tasks = $.JSON.parse(data).map((task) => {
          return { value: task.value, display: task.label };
        });
        this.setState({
          availableTasks: [{ value: "", display: "Select a Task" }].concat(
            tasks
          ),
        });
      })
      .catch((error) => {
        let tasks = TaskData.map((task) => {
          return { value: task.value, display: task.label };
        });
        this.setState({
          availableTasks: [{ value: "", display: "Select a Task" }].concat(
            tasks
          ),
        });
      });
  }

  // properties: either a string or array of strings
  // values: any value or an array of any values
  // if multiple properties, their index must correspond to value index
  changeChannelState(channelIndex, properties, values) {
    // Reusable shallow copy logic to avoid mutating state for updates
    let channels = [...this.state.channels];
    let channel = { ...channels[channelIndex] };
    // If we get a single property to change
    if (typeof properties === "string") {
      channel[properties] = values;
    }
    // If we are given multiple properties to change
    else if (Array.isArray(properties)) {
      for (let i = 0; i < properties.length; i++) {
        channel[properties[i]] = values[i];
      }
    }
    channels[channelIndex] = channel;
    this.setState({ channels });
  }

  runModel(ev, type, numForm) {
    ev.preventDefault();
    const { file, task, model } = this.state.channels[numForm];
    let endPoint = "";

    if (type === "preview") {
      endPoint = `/${task}/preview/${model}/5/${numForm}`;
    } else {
      endPoint = `/${task}/${model}/${numForm}`;
    }

    const data = new FormData();
    data.append("file", file);
    fetch(host + endPoint, {
      method: "POST",
      body: data,
    })
      .then((response) => response.json())
      .then((data) => {
        if (type === "preview") {
          this.update_preview(host + data, numForm);
        } else {
          this.update_run(host + data, numForm);
        }
      })
      .catch((error) => {
        this.changeChannelState(numForm, ["running", "error"], ["none", true]);
      });
  }

  update_run(status_url, numForm) {
    // reference for inside of next lexical scope
    const that = this;
    // send GET request to status URL
    $.getJSON(status_url, function (data) {
      // update UI
      if (data["state"] !== "PENDING" && data["state"] !== "PROGRESS") {
        if ("id" in data) {
          // show result

          that.changeChannelState(
            numForm,
            ["running", "taskId", "success"],
            ["none", data["id"], true]
          );

          that.handleTimeTakenChange(numForm, Number(data["time"]));
        } else {
          // something unexpected happened
          that.changeChannelState(
            numForm,
            ["running", "error"],
            ["none", true]
          );
        }
      } else {
        // rerun in 2 seconds

        setTimeout(() => {
          that.update_run(status_url, numForm);
        }, 10000);
      }
    });
  }

  update_preview(status_url, numForm) {
    // reference for inside of next lexical scope
    const that = this;
    // send GET request to status URL
    $.getJSON(status_url, function (data) {
      if (data["state"] !== "PENDING" && data["state"] !== "PROGRESS") {
        if ("preview" in data) {
          // show result
          let previewString = formatPreview(JSON.parse(data["preview"]));

          // updating channel preview
          that.changeChannelState(
            numForm,
            ["running", "preview", "success"],
            ["none", previewString, true]
          );
        }
        // something unexpected happened
        else {
          this.changeChannelState(
            numForm,
            ["running", "error"],
            ["none", true]
          );
        }
      } else {
        // rerun in 2 seconds
        setTimeout(() => {
          that.update_preview(status_url, numForm);
        }, 10000);
      }
    });
  }

  saveConfig(ev) {
    ev.preventDefault();
    const tasks = [];
    const models = [];
    this.state.channels.forEach((channel) => {
      if (channel.task !== "") tasks.push(channel.task);
      if (channel.model !== "") models.push(channel.model);
    });

    if (tasks.length !== models.length) {
      alert("Partial options cannot be saved.");
    } else {
      let data = JSON.stringify({
        // 'file': window.URL.createObjectURL(this.state.file['file-0']),
        tasks: tasks,
        models: models,
      });
      let bb = new Blob([data], { type: "application/json" });
      let a = document.createElement("a");
      a.download = "selection.json";
      a.href = window.URL.createObjectURL(bb);
      a.click();
    }
  }

  fetchConfig(ev) {
    ev.preventDefault();
    const reader = new FileReader();
    let selection_data = {};
    reader.onload = async (e) => {
      let text = e.target.result;
      if (typeof text !== "string") {
        return;
      }
      try {
        selection_data = JSON.parse(text);
      } catch (e) {
        return;
      }
      if (selection_data.models.length !== 0) {
        let jsonModels = selection_data.models;
        let jsonTasks = selection_data.tasks;

        // updating channel task and model
        while (this.state.channels.length < jsonTasks.length) {
          this.addChannel();
        }

        for (let i = 0; i < jsonTasks.length; i++) {
          this.onTaskChange(i, jsonTasks[i]);
          this.onModelChange(i, jsonModels[i]);
        }
      }
    };

    reader.readAsText(ev.target.files[0]);
    // resetting the inputs value in case user wants to re-enter same file
    ev.target.value = null;
  }

  runAll(ev) {
    ev.preventDefault();

    let channels = [...this.state.channels];
    let indexesToUpdate = [];
    channels.forEach((channel, i) => {
      if (this.isValid(i) && channel.running === "none") {
        indexesToUpdate.push(i);
      }
    });

    // update all our channel states at once to avoid overwrite issues
    for (let i = 0; i < indexesToUpdate.length; i++) {
      const channelToUpdate = { ...channels[indexesToUpdate[i]] };
      channelToUpdate.running = "full";
      channelToUpdate.success = false;
      channelToUpdate.error = false;
      channels[indexesToUpdate[i]] = channelToUpdate;
    }

    this.setState({ channels });

    this.state.channels.map((channel, i) => {
      if (this.isValid(i) && channel.running === "none") {
        return this.runModel(ev, "run", i);
      }
      return null;
    });
  }

  downloadFile(ev, numForm) {
    ev.preventDefault();
    const taskId = this.state.channels[numForm].taskId;
    if (taskId === undefined) {
      alert("No file available for download.");
      return;
    }
    fetch(host + `/celery/fileDownload/${taskId}`, {
      method: "GET",
      headers: {
        "Content-Type": "text/csv",
      },
      responseType: "blob",
    })
      .then((response) => response.blob())
      .then((blob) => {
        let url = window.URL.createObjectURL(blob);
        let a = document.createElement("a");
        a.href = url;
        a.download = `channel_${this.state.channels[numForm].name}.txt`;
        document.body.appendChild(a); // we need to append the element to the dom -> otherwise it will not work in firefox
        a.click();
        a.remove(); //afterwards we remove the element again
      })
      .catch((err) => {
        console.log(err);
      });
  }

  isValid(numForm) {
    const { file, task, model } = this.state.channels[numForm];
    if (
      file === null ||
      task === "Select A Task" ||
      model === "Select A Model"
    ) {
      return false;
    } else {
      return true;
    }
  }

  onFileChange(numForm, file) {
    this.changeChannelState(numForm, "file", file);
  }

  onTaskChange(numForm, value) {
    if (value === "") return;
    fetch(host + "/config/models/" + value)
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        let modelsFromApi = JSON.parse(data).models.map((model) => {
          return { value: model.value, display: model.label };
        });
        // updating our channel models
        this.changeChannelState(
          numForm,
          ["task", "availableModels"],
          [value, modelsFromApi]
        );
      })
      .catch((error) => {
        if (value !== "ner") return;
        let modelsFromApi = ModelData.map((model) => {
          return { value: model.value, display: model.label };
        });
        // updating our channel models
        this.changeChannelState(numForm, "availableModels", modelsFromApi);
      });
  }

  onModelChange(numForm, value) {
    this.changeChannelState(numForm, "model", value);
  }

  handleTimeTakenChange(numForm, time_taken) {
    this.setState({
      time_taken: {
        // object that we want to update
        ...this.state.time_taken, // keep all other key-value pairs
        [numForm]: time_taken,
      },
    });
  }

  addChannel() {
    const nameList = ["A", "B", "C", "D"];
    const createChannel = (name) => {
      return {
        name: name,
        file: null,
        task: "",
        model: "",
        taskId: "",
        availableModels: [],
        preview: "",
        running: "none",
        success: false,
        error: false,
      };
    };

    // identify which index needs to be filled
    const newChannels = [];
    let insertedBefore = false;
    for (let i = 0; i < this.state.channels.length; i++) {
      // if we see an entry that is out-of-order with respect to namelist
      if (this.state.channels[i].name !== nameList[i]) {
        insertedBefore = true;
        // create and push our new channel
        const newChannel = createChannel(nameList[i]);
        newChannels.push(newChannel);

        // push rest of channels behind new channel
        this.state.channels
          .slice(i)
          .forEach((channel) => newChannels.push(channel));
        break;
      } else {
        newChannels.push(this.state.channels[i]);
      }
    }
    // if we are inserting at the end of the list ( nothing was out of order )
    if (!insertedBefore) {
      const newChannel = createChannel(nameList[this.state.channels.length]);
      newChannels.push(newChannel);
    }
    this.setState({ channels: newChannels });
  }

  removeChannel(name) {
    this.setState({
      channels: [
        ...this.state.channels.filter((channel) => channel.name !== name),
      ],
    });
  }

  render() {
    return (
      <>
        <Router>
          <NavBar />
          <Switch>
            <Route
              exact
              path="/"
              render={() => (
                <Home
                  channels={this.state.channels}
                  tasks={this.state.availableTasks}
                  time_taken={this.state.time_taken}
                  onTimeTakenChange={this.handleTimeTakenChange}
                  isValid={this.isValid}
                  addChannel={this.addChannel}
                  removeChannel={this.removeChannel}
                  onModelChange={this.onModelChange}
                  onTaskChange={this.onTaskChange}
                  onFileChange={this.onFileChange}
                  runModel={this.runModel}
                  downloadFile={this.downloadFile}
                  runAll={this.runAll}
                  saveConfig={this.saveConfig}
                  fetchConfig={this.fetchConfig}
                  changeChannelState={this.changeChannelState}
                />
              )}
            />
            <Route
              path="/metrics"
              render={() => (
                <Metrics
                  channels={this.state.channels}
                  time_taken={this.state.time_taken}
                />
              )}
            />
            <Route path="/history" component={History} />
          </Switch>
        </Router>
      </>
    );
  }
}

export default App;
