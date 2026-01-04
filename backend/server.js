const http = require("http");
const app = require("./app");
const { Server } = require("socket.io");

const PORT = process.env.PORT || 5000;

const server = http.createServer(app);

const io = new Server(server, {
  cors: { origin: "*" }
});

io.on("connection", (socket) => {
  console.log("WebSocket connected:", socket.id);

  socket.on("disconnect", () => {
    console.log("WebSocket disconnected:", socket.id);
  });
});

server.listen(PORT, () => {
  console.log(`Backend running on port ${PORT}`);
});
