import {HttpClient} from "@angular/common/http";
import {Injectable} from "@angular/core";
import {Observable, tap} from "rxjs";
import {CookieService} from "../cookie.service";
import {LevelValidationResult} from "../../models/levelValidationResult";

@Injectable({
  providedIn: 'root'
})
export class ValidationService {
  constructor(private httpClient: HttpClient, private cookieService: CookieService) {
  }

  validateTask(level: number, task: number): Observable<LevelValidationResult> {
    return this.httpClient.get<LevelValidationResult>("/api/levels/" + level + "/tasks/" + task + "/validate?uuid="+this.cookieService.getCookie("uuid")).pipe(
      tap((response: LevelValidationResult) => {
        if (response.isValid) {
          let highestLevel = response.level != "1.1" ? this.cookieService.getCookie("highestValidatedLevel") : "0.0";
          if (highestLevel == null) highestLevel = "0.0";
          if (response.level.localeCompare(highestLevel) > 0) {
            this.cookieService.createCookie("highestValidatedLevel", response.level, 365)
          }
        }
      })
    )
  }

  validateTaskWithPayload(level: number, task: number, payload: Map<string, any>): Observable<LevelValidationResult> {
    return this.httpClient.post<LevelValidationResult>("/api/levels/" + level + "/tasks/" + task + "/validate?uuid="+this.cookieService.getCookie("uuid"), {...payload}).pipe(
        tap((response: LevelValidationResult) => {
          if (response.isValid) {
            let highestLevel = response.level != "1.1" ? this.cookieService.getCookie("highestValidatedLevel") : "0.0";
            if (highestLevel == null) highestLevel = "0.0";
            if (response.level.localeCompare(highestLevel) > 0) {
              this.cookieService.createCookie("highestValidatedLevel", response.level, 365)
            }
          }
        })
    )
  }

}
