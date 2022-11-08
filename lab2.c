/* Swarthmore College, CS 43, Lab 2
* Copyright (c) 2022 Swarthmore College Computer Science Department,
* Swarthmore PA
* Professor Kevin Webb */

#include <errno.h>
#include <netinet/in.h>
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/select.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#include <dirent.h>

#define BACKLOG (10)

/* Your program should take two arguments:
* 1) The port number on which to bind and listen for connections, and
* 2) The directory out of which to serve files.
*/

void sendAll(int socket, char *message, int total) {
  int sent = 0;
  int bytes;

  do {
    bytes = send(socket, message+sent, total-sent, 0);
    if(bytes  < 0) {
      perror("ERROR connecting");
      exit(1);
    }
    if(bytes == 0){
      break;
    }
    sent+=bytes;
  } while (sent < total);

}

char* checkRegFile(char *root){
  if(strstr(root, ".html") != NULL){
    return ".html";
  }

  if(strstr(root, ".txt") != NULL){
    return ".txt";
  }

  if(strstr(root, ".jpeg") != NULL){
    return ".jpeg";
  }

  if(strstr(root, ".jpg") != NULL){
    return ".jpg";
  }

  if(strstr(root, ".gif") != NULL){
    return ".gif";
  }

  if(strstr(root, ".png") != NULL){
    return ".png";
  }

  if(strstr(root, ".pdf") != NULL){
    return ".pdf";
  }

  if(strstr(root, ".ico") != NULL){
    return ".ico";
  }

  return NULL;
}

void DNE(int sock, char *path){
  char message[4096];
  sprintf(message, "HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n<!DOCTYPE html>\n<html>\n<head>\n<title>ERROR</title>\n</head>\n<body>\n<h1>404 Page Not Found</h1>\n</body>\n</html>");
  int total = strlen(message);
  sendAll(sock, message, total);
  perror("404 File Not Found");

}

void dir_w_o_index(int sock, char *path){
  DIR *dir;
  struct dirent *dp;

  printf("This is the path: %s", path);
  if((dir = opendir(path)) == NULL) {
    perror("\nCannot open dir\n");
    exit(1);
  }

  char message[4096];
  strcpy(message, "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<!DOCTYPE html>\n<html>\n<head>\n<title>Directory Listing</title>\n</head>\n<body>\n<h1>Directory listing for: ");
  strcat(message, path);
  strcat(message, "</h1><br/><ul>");
  while((dp = readdir(dir)) != NULL) {
    printf("%s\n", dp->d_name);
    strcat(message, "<li><a href=\"");
    strcat(message, dp->d_name);
    strcat(message, "/\">");
    strcat(message, dp->d_name);
    if(checkRegFile(dp->d_name) == NULL){
      strcat(message, "/"); 
    }
    strcat(message, "</a></li>");

  }
  strcat(message, "</ul></html>");
  int total = strlen(message);
  sendAll(sock, message, total);
}

void dir_w_index(int sock, char *path){
  FILE *file;
  char buff[4096];

  file = fopen(path, "r");
  if((file = fopen(path, "r")) == NULL) {
    perror("Cannot open file");
    exit(1);
  }

  char header[200] = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n";
  int total = strlen(header);
  sendAll(sock, header, total);
  int read;
  while((read = fread(buff, 1, sizeof(buff), file)) != 0) {
    sendAll(sock, buff, read);
  }
}


void regFile (int sock, char *path, char *type){
  char header[4096];
  strcpy(header, "HTTP/1.1 200 OK\r\nContent-Type: ");
  strcat(header, type);
  strcat(header, "\r\n\r\n");

  FILE *file;
  char buff[4096];
  file = fopen(path, "r");
  if((file = fopen(path, "r")) == NULL) {
    perror("Cannot open file");
    exit(1);
  }

  int total = strlen(header);
  sendAll(sock, header, total);
  int read;
  while((read = fread(buff, 1, sizeof(buff), file)) != 0) {
    sendAll(sock, buff, read);
  }
}

/* Function:
Receives and parses request
Determines case and sends to helper funtion
*/
void process_client(int server_sock) {
  int bytes = 0;
  char request[4096];
  char *ret;
  int received = 0;
  int size = 4096;
  char *path;
  char *cpy_path;
  char *delim = " ";
  FILE *file;

  path = malloc(sizeof(char *)*(4100));
  if(path == NULL) {
    perror("Error: Malloc Failed");
    exit(1);
  }
  cpy_path = malloc(sizeof(char *)*(4100));
  if(cpy_path == NULL) {
    perror("Error: Malloc Failed");
    exit(1);
  }

  // Receives message
  do {
    bytes = recv(server_sock, request+received, size-received, 0);
    if(bytes < 0) {
      perror("ERROR connecting");
      exit(1);
    }
    if(bytes == 0){
      break;
    }
    received+=bytes;
    ret = strstr(request, "\r\n\r\n");
  } while (ret == NULL);

  // Gets the path
  received = 0;
  char *token = strtok(request, delim);
  token = strtok(NULL, delim);
  path = token;
  path = path + 1;
  strcpy(cpy_path, path);
  printf("This is our path: |%s|\n", path);

  struct stat buffer;
  int status = stat(path, &buffer);
  // Case 1: File/Directory does not exist
  if(status != 0){
    printf("-1, stat error");
    DNE(server_sock, path);
  }

  int status_type = S_ISDIR(buffer.st_mode); // Returns 1 if true
  // Case 2: Path is a regular file
  if (status_type == 0){
    // Determines the type of the file
    char type[100];
    strcpy(type, checkRegFile(path));
    printf("The type of the file is: %s\n", type);
    regFile(server_sock, path, type);
  }
  else if (status_type != 0){
    strcat(cpy_path, "/index.html");
    //Case 3: Path is a directory and includes a index.html file
    if ((file = fopen(cpy_path, "r"))){
      fclose(file);
      dir_w_index(server_sock, cpy_path);
    }
    // Case 4: Path is a directory, but does not include a index.html file
    else {
      dir_w_o_index(server_sock, path);
    }
  }
}

void *thread_function(void *server_sock) {
  int *argument = (int *) server_sock;
  int id = *argument;

  process_client(id);

  free(argument);
  return NULL;
}

int main(int argc, char **argv) {
  /* For checking return values. */
  int retval;

  /* To store the user-specified port. */
  int port;

  /* The socket to bind/listen/accept on. */
  int server_sock;

  /* A flag to pass to turn on the SO_REUSEADDR option. */
  int reuse_true;


  /* Make sure we get the right number of arguments. */
  if (argc != 3) {
    printf("Usage: %s <port> <document root>\n", argv[0]);
    exit(1);
  }

  /* Read the port number from the first command line argument. */
  port = atoi(argv[1]);
  if (chdir(argv[2])) {
    perror("chdir fail");
    exit(1);
  }

  printf("Webserver configuration:\n");
  printf("\tPort: %d\n", port);
  printf("\tDocument root: %s\n", argv[2]);

  /* Create a socket to which clients will connect. */
  server_sock = socket(AF_INET, SOCK_STREAM, 0);
  if (server_sock < 0) {
    perror("Creating socket failed");
    exit(1);
  }

  /* A server socket is bound to a port, which it will listen on for incoming
  * connections.  By default, when a bound socket is closed, the OS waits a
  * couple of minutes before allowing the port to be re-used.  This is
  * inconvenient when you're developing an application, since it means that
  * you have to wait a minute or two after you run to try things again, so
  * we can disable the wait time by setting a socket option called
  * SO_REUSEADDR, which tells the OS that we want to be able to immediately
  * re-bind to that same port. See the socket(7) man page ("man 7 socket")
  * and setsockopt(2) pages for more details about socket options. */
  reuse_true = 1;
  retval = setsockopt(server_sock, SOL_SOCKET, SO_REUSEADDR, &reuse_true,
    sizeof(reuse_true));
    if (retval < 0) {
      perror("Setting socket option failed");
      exit(1);
    }

    /* Create an address structure.  This is very similar to what we saw on the
    * client side, only this time, we're not telling the OS where to connect,
    * we're telling it to bind to a particular address and port to receive
    * incoming connections.  Like the client side, we must use htons() to put
    * the port number in network byte order.  When specifying the IP address,
    * we use a special constant, INADDR_ANY, which tells the OS to bind to all
    * of the system's addresses.  If your machine has multiple network
    * interfaces, and you only wanted to accept connections from one of them,
    * you could supply the address of the interface you wanted to use here. */
    struct sockaddr_in addr;
    addr.sin_family = AF_INET;
    addr.sin_port = htons(port);
    addr.sin_addr.s_addr = INADDR_ANY;

    /* Call bind.  As its name implies, this system call asks the OS to
    * bind the socket to the address and port specified above. Be sure to
    * check for errors.  On failure, call perror("bind") to get a
    * human-readable description of the error and then terminate. You can cast
    * the address of the "addr" struct defined above to a (struct sockaddr *)
    * when passing it to bind. */
    retval = bind(server_sock, (struct sockaddr *) &addr, sizeof(addr));
    if (retval < 0) {
      perror("Bind failed");
      exit(1);
    }

    /* Call listen. Now that we've bound to an address and port, we tell
    * the OS that we're ready to start listening for client connections.  This
    * effectively activates the server socket.  BACKLOG (#defined above) tells
    * the OS how much space to reserve for incoming connections that have not
    * yet been accepted. Similar to bind, check for errors and call
    * perror("listen") for human-readable details. */
    retval = listen(server_sock, BACKLOG);
    if (retval < 0) {
      perror("listen failed");
      exit(1);
    }

    while (1) {
      /* Declare a socket for the client connection. */
      int sock;

      /* Another address structure.  This time, the system will automatically
      * fill it in, when we accept a connection, to tell us where the
      * connection came from. */
      struct sockaddr_in remote_addr;
      unsigned int socklen = sizeof(remote_addr);

      /* Accept the first waiting connection from the server socket and
      * populate the address information.  The result (sock) is a socket
      * descriptor for the conversation with the newly connected client.  If
      * there are no pending connections in the back log, this function will
      * block indefinitely while waiting for a client connection to be made.
      * */
      sock = accept(server_sock, (struct sockaddr *) &remote_addr, &socklen);

      if (sock < 0) {
        perror("Error accepting connection");
        exit(1);
      }

      // Start creating threads for multiple clients
      pthread_t new_thread;
      int *argument = malloc(sizeof(int));
      *argument = sock;
      retval = pthread_create(&new_thread, NULL, thread_function, argument);
      if (retval) {
        printf("pthread_create() failed\n");
        exit(1);
      }

      retval = pthread_detach(new_thread);
      if (retval) {
        printf("pthread_detach() failed\n");
        exit(1);
      }
      usleep(500000);

      /* At this point, you have a connected client socket (named sock) that
      * you can use to send() and recv(). */

      /* Tell the OS to clean up the resources associated with that client
      * connection, now that we're done with it. */
      close(sock);
    }
    close(server_sock);
  }
