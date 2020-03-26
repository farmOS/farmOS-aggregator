<template>
    <v-dialog
            v-model="requestAuthorizationDialog"
            max-width="600"
    >
        <v-card>
            <v-card-title class="headline">Request Authorization</v-card-title>

            <v-card-text>
                Input the email to send a authorization link. This should be the farmOS admin email.

                <v-text-field type="email" label="farmOS Admin Email" v-model="userEmail"></v-text-field>

                OR

                <v-btn
                        class="ma-2"
                        :loading="authorizationLinkLoading"
                        :disabled="authorizationLinkLoaded"
                        color="secondary"
                        @click="generateAuthorizationLink()"
                >
                    Generate authorization Link
                </v-btn>

                <v-text-field
                        label="Authorization Link"
                        v-if="authorizationLinkLoaded"
                        v-model="authorizationLink"
                        readonly
                ></v-text-field>
            </v-card-text>

            <v-card-actions>
                <v-spacer></v-spacer>

                <v-btn
                        color="green darken-1"
                        text
                        @click="requestauthorizationDialog = false"
                >
                    Cancel
                </v-btn>

                <v-btn
                  color="green darken-1"
                  text
                  @click="authorizeNow()"
                >
                    Authorize Now
                </v-btn>

                <v-btn
                        color="green darken-1"
                        text
                        :disabled="authorizationEmailLoading || authorizationEmailSent"
                        @click="sendAuthorizationEmail()"
                >
                    Send
                </v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script lang="ts">
    import { Component, Vue, Prop } from 'vue-property-decorator';
    import { dispatchCreateFarmAuthLink, dispatchSendFarmAuthorizationEmail } from '@/store/farm/actions';

    @Component
    export default class FarmRequestauthorizationDialog extends Vue {
        @Prop({default: false}) public farmID!: number;

        public requestAuthorizationDialog: boolean = false;
        public authLink: string = '';
        public userEmail: string = '';

        // Properties for the authorization Request Email.
        public authorizationEmailLoading: boolean = false;
        public authorizationEmailSent: boolean = false;

        // Properties for the authorization Generate Link.
        public authorizationLinkLoading: boolean = false;
        public authorizationLinkLoaded: boolean = false;
        public authorizationLink: string = '';

        public async authorizeNow(farmID) {
            await this.generateAuthorizationLink().then( (res) => {
                // Redirect to the authorization page.
                window.open(this.authorizationLink);
            });
        }

        public async generateAuthorizationLink() {
            // Query the API to get an authorization link with an API token embedded in the query params.
            this.authorizationLinkLoading = true;
            const link = await dispatchCreateFarmAuthLink(this.$store, { farmID: this.farmID });
            if (link) {
                this.authorizationLink = link;
                this.authorizationLinkLoaded = true;
            }
            this.authorizationLinkLoading = false;
        }

        public async sendAuthorizationEmail() {

            this.authorizationEmailLoading = true;
            await dispatchSendFarmAuthorizationEmail(
              this.$store,
              {emailTo: this.userEmail, farmID: this.farmID},
            ).then((success) => {
                this.authorizationEmailLoading = false;
                this.authorizationEmailSent = true;
              }, (failure) => {
                this.authorizationEmailLoading = false;
                this.authorizationEmailSent = false;
              },
            );
        }

        public openDialog() {
            this.requestAuthorizationDialog = true;
            this.authorizationEmailSent = false;
            this.userEmail = '';
        }

        public closeDialog() {
            this.requestAuthorizationDialog = false;
        }

    }


</script>
