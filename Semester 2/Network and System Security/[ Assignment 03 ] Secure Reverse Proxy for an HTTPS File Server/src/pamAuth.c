#include "pamAuth.h"
#include "utils.h"
#include <security/pam_appl.h>
#include <security/pam_misc.h>
#include <stdio.h>
#include <string.h>

static int pamConv(int numMsg, const struct pam_message** msg, struct pam_response** resp, void* appdata) {
    char* password = (char*)appdata;
    *resp = calloc(numMsg, sizeof(struct pam_response));
    for (int i = 0; i < numMsg; i++) {
        if (msg[i]->msg_style == PAM_PROMPT_ECHO_OFF) {
            (*resp)[i].resp = strdup(password);
        }
    }
    return PAM_SUCCESS;
}

int authenticateUser(const char* username, const char* password) {
    pam_handle_t* pamh;
    struct pam_conv conv = {pamConv, (void*)password};
    int ret = pam_start("login", username, &conv, &pamh);
    if (ret != PAM_SUCCESS) return 0;

    ret = pam_authenticate(pamh, 0);
    if (ret != PAM_SUCCESS) {
        pam_end(pamh, ret);
        return 0;
    }

    ret = pam_acct_mgmt(pamh, 0);
    pam_end(pamh, ret);
    return ret == PAM_SUCCESS;
}

int handleLogin(SSL* ssl) {
    char username[256], password[256];

    sendMessage(ssl, "Username: ");
    int len = receiveMessage(ssl, username, sizeof(username));
    if (len <= 0) return 0;
    username[len - 1] = '\0'; // Remove newline

    sendMessage(ssl, "Password: ");
    len = receiveMessage(ssl, password, sizeof(password));
    if (len <= 0) return 0;
    password[len - 1] = '\0'; // Remove newline

    return authenticateUser(username, password);
}