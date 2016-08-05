/*
 * Copyright (c) 2016 by cisco Systems, Inc.
 * All rights reserved.
 */
package util

import "os"
import "fmt"

func GetServerIPPort() (string, string) {
    server := os.Getenv("SERVER_IP")
    if server == "" {
        fmt.Printf("Could not read env SERVER_IP")
        os.Exit(-1)
    }

    port := os.Getenv("SERVER_PORT")
    if port == "" {
        fmt.Printf("Could not read env SERVER_PORT")
        os.Exit(-1)
    }

    fmt.Printf("Using SERVER IP PORT: %s:%s\n", server, port)

    return server, port
}
