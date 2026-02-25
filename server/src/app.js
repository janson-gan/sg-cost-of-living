const express = require("express");
const cors = require("cors");
const helmet = require("helmet");
const morgan = require("morgan");
require("dotenv").config();

const pool = require("./config/db");

const app = express();

const PORT = process.env.PORT || 3001;

// Middleware
app.use(cors());
app.use(helmet());
app.use(morgan("dev"));
app.use(express.json());

// Health check endpoint
app.get("/api/v1/health", async (req, res) => {
  try {
    const db_result = await pool.query("SELECT NOW()");
    res.json({
      status: "ok",
      timestamp: new Date().toISOString(),
      services: {
        database: "connected",
        db_time: db_result.rows[0].now,
      },
    });
  } catch (err) {
    res.status(503).json({
      status: "error",
      services: {
        database: "disconnected",
      },
    });
  }
});

// Placeholder for other routes
app.get("/api/v1/dashboard/kpis", (req, res) => {
  res.json({ success: true, data: [], message: "KPI data endpoint" });
});

app.get("/api/v1/hdb/transactions", (req, res) => {
  res.json({ success: true, data: [], message: "HDB transactions endpoint" });
});

app.get("/api/v1/hdb/trends", (req, res) => {
  res.json({ success: true, data: [], message: "HDB trends endpoint" });
});

app.get("/api/v1/hdb/map-data", (req, res) => {
  res.json({ success: true, data: [], message: "HDB map data endpoint" });
});

app.get("/api/v1/coe/trends", (req, res) => {
  res.json({ success: true, data: [], message: "COE trends endpoint" });
});

app.get("/api/v1/cpi/trends", (req, res) => {
  res.json({ success: true, data: [], message: "CPI trends endpoint" });
});

app.listen(PORT, () => {
  console.log(
    `Server running on http://localhost:${PORT}`,
  );
  console.log(
    `Health check: http://localhost:${PORT}/api/v1/health`,
  );
});

module.exports = app;
