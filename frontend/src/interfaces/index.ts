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

export interface ApiKey {
    id: number;
    time_created: string;
    key: string;
    enabled: boolean;
    name: string;
    notes: string;
    farm_id: number[];
    all_farms: boolean;
    scopes: string[];
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
    notes?: string;
    tags?: string;
    info?: object[];
    scope?: string;
    active?: boolean;

    is_authorized: boolean;
    auth_error?: string;
    token: FarmToken;
}

export interface FarmInfo {
    name?: string;
    url?: string;
    api_version?: string;
}

export interface FarmProfileUpdate {
    farm_name?: string;
    url?: string;
    notes?: string;
    tags?: string;
    active?: boolean;
    scope?: string;
}

export interface FarmProfileCreate {
    farm_name: string;
    url: string;
    notes?: string;
    tags?: string;
    token?: FarmToken;
    active?: boolean;
    scope?: string;
}

export interface FarmProfileAuthorize {
    grant_type: string;
    code: string;
    state: string;
    client_id: string;
    client_secret?: string;
    redirect_uri?: string;
    scope?: string;
}

export interface FarmAuthorizationNonce {
    apiToken?: string;
    state?: string;
    farmId?: number;
    farmUrl?: string;
    scopes?: string[];
}
