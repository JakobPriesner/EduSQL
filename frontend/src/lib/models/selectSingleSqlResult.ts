import {SqlResult} from "./sqlResult";

export interface SelectSingleSqlResult extends SqlResult{
    operation: string
    result?: {[key: string]: any }
    errors: string
}