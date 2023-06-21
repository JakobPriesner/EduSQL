import {SqlResult} from "./sqlResult";

export interface SelectAllSqlResult extends SqlResult{
    operation: string
    result?: Array<{[key: string]: any }>
    errors: string
}