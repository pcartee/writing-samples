/* Sample code for integrate.tdx.cli 12/08/2023 */

```go
/*
 *   Copyright (c) 2023 Intel Corporation
 *   All rights reserved.
 *   SPDX-License-Identifier: BSD-3-Clause
 */
package main

import (
	"crypto/tls"
	"flag"
	"fmt"
	"os"
	"os/exec"

	"github.com/intel/trustauthority-client-for-go/go-connector"
	"github.com/pkg/errors"
)

func main() {
	var policyId string
	cfg := client.Config{
		TlsCfg: &tls.Config{
			InsecureSkipVerify: true,
		},
	}

	flag.StringVar(&cfg.Url, "url", "", "Base URL of Intel Trust Authority SaaS")
	flag.StringVar(&cfg.ApiKey, "key", "", "Api Key")
	flag.StringVar(&policyId, "pid", "", "Policy ID for verification")
	flag.Parse()

	client, err := client.New(&cfg)
	if err != nil {
		panic(err)
	}

	// optional: either caller can provide existing public key or create new using trustauthority-cli create-key-pair command
	pubPath := "pub.pem"
	_, err = createRSAKeypair(pubPath)
	if err != nil {
		panic(err)
	}

	// trustauthority-cli looks for API URL and API Key in environment
	os.Setenv("TRUSTAUTHORITY_URL", cfg.Url)
	os.Setenv("TRUSTAUTHORITY_API_KEY", cfg.ApiKey)

	// pubPath: public key to be used as reportdata for quote generation
	out, err := exec.Command("amtrustauthorityber-cli", "token", "--policy-ids", policyId, "-f", pubPath).Output()
	if err != nil {
		panic(err)
	}
	token := out[:]

	fmt.Printf("TOKEN: %s\n", string(token))

	// it is best practice to always clear secrets from environment after use
	os.Unsetenv("TRUSTAUTHORITY_URL")
	os.Unsetenv("TRUSTAUTHORITY_API_KEY")

	parsedToken, err := client.VerifyToken(string(token))
	if err != nil {
		panic(err)
	}

	fmt.Printf("CLAIMS: %+v\n", parsedToken.Claims)
}

func createRSAKeypair(pubPath string) ([]byte, error) {

	out, err := exec.Command("trustauthority-cli", "create-key-pair", "-f", pubPath).Output()
	if err != nil {
		return nil, errors.Wrap(err, "Failed to execute trustauthority-cli create-key-pair command")
	}
	return out[:], nil
}
```