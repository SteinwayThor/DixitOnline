import { io } from "socket.io-client"
import { backend_url } from "./backendUrl"

const socket = io(backend_url);

export default socket
