import {SqlResult} from "./sqlResult";

export interface UpdateSqlResult extends SqlResult{
    operation: string
    result?: number
    errors: string
}