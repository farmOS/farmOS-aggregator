<template>
    <v-dialog
            v-model="requestRegistrationDialog"
            max-width="600"
    >
        <v-card>
            <v-card-title class="headline">Request Registration</v-card-title>

            <v-card-text>
                Input the email to send a registration link. This should be the farmOS admin email.

                <v-text-field type="email" label="farmOS Admin Email" v-model="userEmail"></v-text-field>

                OR

                <v-btn
                        class="ma-2"
                        :loading="registrationLinkLoading"
                        :disabled="registrationLinkLoaded"
                        color="secondary"
                        @click="generateRegistrationLink()"
                >
                    Generate Registration Link
                </v-btn>

                <v-text-field
                        label="Authorization Link"
                        v-if="registrationLinkLoaded"
                        v-model="registrationLink"
                        readonly
                ></v-text-field>
            </v-card-text>

            <v-card-actions>
                <v-spacer></v-spacer>

                <v-btn
                        color="green darken-1"
                        text
                        @click="requestRegistrationDialog = false"
                >
                    Cancel
                </v-btn>

                <v-btn
                        color="green darken-1"
                        text
                        :disabled="registrationEmailLoading || registrationEmailSent"
                        @click="sendRegistrationEmail()"
                >
                    Send
                </v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script lang="ts">
    import { Component, Vue, Prop } from 'vue-property-decorator';
    import { dispatchCreateFarmRegistrationLink, dispatchSendFarmRegistrationEmail } from '@/store/farm/actions';

    @Component
    export default class FarmRequestRegistrationDialog extends Vue {
        public requestRegistrationDialog: boolean = false;

        public userEmail: string = '';

        // Properties for the Registration Request Email.
        public registrationEmailLoading: boolean = false;
        public registrationEmailSent: boolean = false;

        // Properties for the Registration Generate Link.
        public registrationLinkLoading: boolean = false;
        public registrationLinkLoaded: boolean = false;
        public registrationLink: string = '';

        public async generateRegistrationLink() {
            // Query the API to get an Registration link with an API token embedded in the query params.
            this.registrationLinkLoading = true;
            const link = await dispatchCreateFarmRegistrationLink(this.$store);
            if (link) {
                this.registrationLink = link;
                this.registrationLinkLoaded = true;
            }
            this.registrationLinkLoading = false;
        }

        public async sendRegistrationEmail() {

            this.registrationEmailLoading = true;
            await dispatchSendFarmRegistrationEmail(
              this.$store,
              {emailTo: this.userEmail},
            ).then((success) => {
                this.registrationEmailLoading = false;
                this.registrationEmailSent = true;
              }, (failure) => {
                this.registrationEmailLoading = false;
                this.registrationEmailSent = false;
              },
            );
        }

        public openDialog() {
            this.requestRegistrationDialog = true;
            this.registrationEmailSent = false;
            this.userEmail = '';
        }

        public closeDialog() {
            this.requestRegistrationDialog = false;
        }

    }


</script>
