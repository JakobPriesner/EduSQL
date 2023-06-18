import {HttpClient} from "@angular/common/http";
import {Injectable} from "@angular/core";
import {Observable, tap} from "rxjs";
import {CookieService} from "../cookie.service";
import {RegisterUserResponse} from "../../models/registerUserResponse";
import {GetUserResponse} from "../../models/getUserResponse";
import {DbUser} from "../../models/dbUser";

@Injectable({
  providedIn: 'root'
})
export class UsersService {
  constructor(private httpClient: HttpClient, private cookieService: CookieService) {
  }

  checkIfUserExists(uuid: string): Observable<GetUserResponse> {
    return this.httpClient.get<GetUserResponse>("/api/users/me?uuid=" + uuid);
  }

  checkIfDbUserExists(dbUser: DbUser) : Observable<GetUserResponse> {
    return this.httpClient.post<GetUserResponse>("/api/users/db-user?uuid=" + this.cookieService.getCookie("uuid"), dbUser);
  }

  registerUser(): Observable<RegisterUserResponse> {
    return this.httpClient.post<RegisterUserResponse>("/api/users/register", {}).pipe(
      tap((response: RegisterUserResponse) => {
        const userUuid = response.userUuid;
        this.cookieService.createCookie('uuid', userUuid, 7);
      })
    );
  }

}
