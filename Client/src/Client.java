// Client connecting to server

import java.io.IOException;
import java.net.*;

public class Client {
    private Socket clientSock;

    public void startConnection(String ip, int port) {
        try {
            clientSock = new Socket(ip, port);
        }
        catch (IOException e) {
            e.printStackTrace();
        }

    }

    public void closeConnection() {
        try {
            clientSock.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        System.out.println("Client run");
        Client c = new Client();
        c.startConnection("127.0.0.1", 5000);   // !!! which IP address to connect to?
    }

}
