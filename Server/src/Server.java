import java.io.*;
import java.net.*;

public class Server {

    private ServerSocket serverSocket;

    public Server(int port) {
        try {
            serverSocket = new ServerSocket(port);
            serverSocket.setSoTimeout(1000000);  // !!! need this or nah?
        }
        catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void runServer() {
        try {
            System.out.println("Waiting for client on port " + serverSocket.getLocalPort());
            Socket server = serverSocket.accept();
            System.out.println("Connected to " + server.getRemoteSocketAddress());

            // !!! do things


            server.close();

        }
        catch (SocketTimeoutException e) {
            System.out.println("Socket timed out");
        }
        catch (IOException e) {
            e.printStackTrace();
        }

    }

    public static void main(String[] args) {
        System.out.println("Server run");
        Server s = new Server(5000);    // !!! magic number
        s.runServer();

    }
}
