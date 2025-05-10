#include "pamAuth.h"
#include "utils.h"
#include <security/pam_appl.h>
#include <security/pam_misc.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

static int pamConv(int numMsg, const struct pam_message** msg, struct pam_response** resp, void* appdata) {
    char* password = (char*)appdata;
    *resp = calloc(numMsg, sizeof(struct pam_response));
    if (!*resp) {
        logError("PAM response allocation failed");
        return PAM_BUF_ERR;
    }
    for (int i = 0; i < numMsg; i++) {
        if (msg[i]->msg_style == PAM_PROMPT_ECHO_OFF) {
            (*resp)[i].resp = strdup(password);
            if (!(*resp)[i].resp) {
                logError("PAM response strdup failed");
                return PAM_BUF_ERR;
            }
        }
    }
    return PAM_SUCCESS;
}

int authenticateUser(const char* username, const char* password) {
    pam_handle_t* pamh = NULL;
    struct pam_conv conv = {pamConv, (void*)password};
    int ret = pam_start("login", username, &conv, &pamh);
    if (ret != PAM_SUCCESS) {
        fprintf(stderr, "PAM start failed: %s\n", pam_strerror(NULL, ret));
        return 0;
    }

    ret = pam_authenticate(pamh, 0);
    if (ret != PAM_SUCCESS) {
        fprintf(stderr, "PAM authentication failed: %s\n", pam_strerror(pamh, ret));
        pam_end(pamh, ret);
        return 0;
    }

    ret = pam_acct_mgmt(pamh, 0);
    if (ret != PAM_SUCCESS) {
        fprintf(stderr, "PAM account management failed: %s\n", pam_strerror(pamh, ret));
        pam_end(pamh, ret);
        return 0;
    }

    pam_end(pamh, PAM_SUCCESS);
    return 1;
}

int handleLogin(SSL* ssl) {
    char username[256], password[256];

    if (sendMessage(ssl, "Username: ") <= 0) {
        logError("Failed to send username prompt");
        return 0;
    }
    int len = receiveMessage(ssl, username, sizeof(username));
    if (len <= 0 || username[0] == '\n' || username[0] == '\0') {
        sendMessage(ssl, "ERROR: Invalid username\n");
        return 0;
    }
    username[strcspn(username, "\n")] = '\0';

    if (sendMessage(ssl, "Password: ") <= 0) {
        logError("Failed to send password prompt");
        return 0;
    }
    len = receiveMessage(ssl, password, sizeof(password));
    if (len <= 0 || password[0] == '\n' || password[0] == '\0') {
        sendMessage(ssl, "ERROR: Invalid password\n");
        return 0;
    }
    password[strcspn(password, "\n")] = '\0';

    if (!authenticateUser(username, password)) {
        sendMessage(ssl, "ERROR: Authentication failed\n");
        return 0;
    }
    return 1;
}