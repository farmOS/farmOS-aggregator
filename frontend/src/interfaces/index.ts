export interface IUserProfile {
    email: string;
    is_active: boolean;
    is_superuser: boolean;
    full_name: string;
    id: number;
}

export interface IUserProfileUpdate {
    email?: string;
    full_name?: string;
    password?: string;
    is_active?: boolean;
    is_superuser?: boolean;
}

export interface IUserProfileCreate {
    email: string;
    full_name?: string;
    password?: string;
    is_active?: boolean;
    is_superuser?: boolean;
}

export interface FarmToken {
    access_token: string;
    refresh_token: string;
    expires_at: string;
    expires_in: string;
}

export interface FarmProfile {
    id: number;
    time_updated?: string;
    time_created?: string;
    last_accessed?: string;
    farm_name: string;
    url: string;
    username: string;
    notes?: string;
    tags?: string;
    info?: object[];
    active?: boolean;

    is_authorized: boolean;
    auth_error?: string;
    token: FarmToken;
}

export interface FarmProfileUpdate {
    farm_name?: string;
    url?: string;
    username?: string;
    password?: string;
    notes?: string;
    tags?: string;
    active?: boolean;
}

export interface FarmProfileCreate {
    farm_name: string;
    url: string;
    username?: string;
    password?: string;
    notes?: string;
    tags?: string;
    token?: FarmToken;
    active?: boolean;
}

export interface FarmProfileAuthorize {
    grant_type: string;
    code: string;
    state: string;
    client_id: string;
    client_secret?: string;
    redirect_uri?: string;
}

export interface FarmAuthorizationNonce {
    apiToken?: string;
    state?: string;
    farmId?: number;
    farmUrl?: string;
    scopes?: string[];
}
