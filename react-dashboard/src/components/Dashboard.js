// src/components/Dashboard.js
import React, { useEffect, useState } from "react";
import axios from "axios";
import { AgGridReact } from "ag-grid-react";
import { ModuleRegistry, AllCommunityModule } from "ag-grid-community";
import "ag-grid-community/styles/ag-grid.css";
import "ag-grid-community/styles/ag-theme-alpine.css"; // or your chosen theme

// Register AG Grid modules
ModuleRegistry.registerModules([AllCommunityModule]);

function Dashboard() {
  const [issues, setIssues] = useState([]);

  const [columnDefs] = useState([
    { headerName: "ID", field: "id", sortable: true, filter: true },
    {
      headerName: "Title",
      field: "title",
      sortable: true,
      filter: true,
      flex: 1,
      cellStyle: { textAlign: "left" },
      autoHeight: true,
      cellClass: "ag-cell-wrap-text",
    },
    {
      headerName: "Label",
      field: "program_name",
      sortable: true,
      filter: true,
      flex: 1,
      cellStyle: { textAlign: "left" },
      autoHeight: true,
      cellClass: "ag-cell-wrap-text",
    },
  ]);

  useEffect(() => {
    axios
      .get("http://localhost:5000/issues")
      .then((res) => setIssues(res.data))
      .catch((err) => console.error("Error fetching issues:", err));
  }, []);

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        height: "80vh",
      }}
    >
      <div className="ag-theme-alpine" style={{ height: 400, width: "80%" }}>
        <h2>GitHub Issues</h2>
        <AgGridReact
          rowData={issues}
          columnDefs={columnDefs}
          pagination={true}
          paginationPageSize={10}
          paginationPageSizeSelector={[10, 20, 50]}
          theme="themeQuartz"
          domLayout="autoHeight"
        />
      </div>
    </div>
  );
}

export default Dashboard;
