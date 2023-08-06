// Copyright (c) FlapMX LLC.
// This source code is licensed under the MIT license found in the
// LICENSE file in the root directory of this source tree.

import React, { useState, useEffect } from "react";

import DataGrid from "../components/DataGrid";

const host = process.env.REACT_APP_BASE_URL;

const History = () => {
  const [pageState, setPageState] = useState({
    page: 1,
    pageSize: 10,
    total: 10,
  });

  const [searchQuery, setSearchQuery] = useState("");
  const [rows, setRows] = useState([]);
  const [selectionId, setSelectionId] = useState([]);
  const [loadingRows, setLoadingRows] = useState(false);

  useEffect(() => {
    // Fetching initial
    setLoadingRows(true);
    fetch(
      host +
        `/celery/history?page_size=${pageState.pageSize}&page_num=${pageState.page}`
    )
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        setRows(data);
        setLoadingRows(false);
      })
      .catch((error) => {
        console.log(error);
      });

    fetch(host + `/celery/history/total`)
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        setPageState({ ...pageState, total: data });
      })
      .catch((error) => {
        console.log(error);
      });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [pageState.page]);

  const downloadFile = () => {
    if (selectionId.length === 0) {
      alert("Please select a record.");
      return;
    }
    fetch(host + `/celery/fileDownload/${selectionId}`, {
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
        a.download = "results.txt";
        document.body.appendChild(a); // we need to append the element to the dom -> otherwise it will not work in firefox
        a.click();
        a.remove(); //afterwards we remove the element again
      })
      .catch((err) => {
        console.log(err);
      });
  };

  const handleInput = (e) => {
    setSearchQuery(e.target.value);
  };

  const handleQuery = () => {
    if (searchQuery.length > 0) {
      fetch(host + `/celery/search/${searchQuery}`)
        .then((response) => {
          return response.json();
        })
        .then((data) => {
          setRows(data);
        })
        .catch((error) => {
          console.log(error);
        });
    } else {
      fetch(
        host +
          `/celery/history?page_size=${pageState.pageSize}&page_num=${pageState.page}`
      )
        .then((response) => {
          return response.json();
        })
        .then((data) => {
          setRows(data);
        })
        .catch((error) => {
          console.log(error);
        });
    }
  };

  const handlePageChange = (direction) => {
    if (direction === "next")
      setPageState({ ...pageState, page: pageState.page + 1 });
    if (direction === "prev")
      setPageState({ ...pageState, page: pageState.page - 1 });
  };

  return (
    <div className="history-container">
      <div className="history-header">
        <div className="search-bar">
          <input
            type="text"
            className="form-control"
            onChange={handleInput}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                handleQuery();
              }
            }}
            value={searchQuery}
            placeholder="Search.."
          />
        </div>
      </div>
      <div className="data-grid-container">
        <DataGrid
          loading={loadingRows}
          rows={rows}
          selectionId={selectionId}
          setSelectionId={setSelectionId}
          downloadFile={downloadFile}
        />
      </div>
      <div className="pagination-div">
        <button
          onClick={() => handlePageChange("prev")}
          disabled={pageState.page === 1}
        >
          <i className="fas fa-arrow-left"></i>
        </button>
        <button
          disabled={pageState.page * pageState.pageSize >= pageState.total}
          onClick={() => handlePageChange("next")}
        >
          <i className="fas fa-arrow-right"></i>
        </button>
        {/* Do we have less rows than our page size? 

          If so- we need to grab what would be our current endIndex ( page * pagesize ) and subtract a page,
          then make up the difference by adding our rows.length.

          If not- we can just use the page * pagesize value to indicate our endIndex. If page is 2 and our pageSize is 5,
          our endIndex would be 10 for example. Flip to the previous page? 1*5 = 5, our endIndex is 5.
       */}
        <p>
          {`${pageState.page * pageState.pageSize - pageState.pageSize + 1} - ${
            rows.length < pageState.pageSize
              ? pageState.page * pageState.pageSize -
                pageState.pageSize +
                rows.length
              : pageState.page * pageState.pageSize
          } of ${pageState.total}`}
        </p>
      </div>
    </div>
  );
};

export default History;
