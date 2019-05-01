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

export interface FarmProfile {
    farm_name: string;
    url: string;
    username: string;
    id: number;
}

export interface FarmProfileUpdate {
    farm_name?: string;
    url?: string;
    username?: string;
    password?: string;
}

export interface FarmProfileCreate {
    farm_name: string;
    url: string;
    username: string;
    password: string;
}
