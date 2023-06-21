export interface SqlResult{
    operation: string;
    result?: Array<{ [key: string]: any }> | number | undefined;
    errors: string;
}