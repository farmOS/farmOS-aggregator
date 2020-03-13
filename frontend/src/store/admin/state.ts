import { IUserProfile, ApiKey } from '@/interfaces';

export interface AdminState {
    users: IUserProfile[];
    apiKeys: ApiKey[];
}
