import {Component, OnInit} from '@angular/core';
import {MatStepper} from "@angular/material/stepper";
import {CookieService} from "../../lib/services/cookie.service";
import {ValidationService} from "../../lib/services/api/validation.service";
import {LocalDbUserValidator} from "../../lib/validator/local-db-user.validator";
import {UserDataStore} from "../../lib/stores/user-data.store";
import {InboxService} from "../../lib/services/api/inbox.service";
import {Message} from "../../lib/models/message.interface";

@Component({
  selector: 'app-level-five',
  templateUrl: './level-five.component.html',
  styleUrls: ['./level-five.component.css']
})
export class LevelFiveComponent implements OnInit{

  errorMessage: string = "";
  highestValidatedLevel: string = this.cookieService.getCookie("highestValidatedLevel") ?? "0.0";

  constructor(public cookieService: CookieService,
              public localDbUserValidator: LocalDbUserValidator,
              public userDataStore: UserDataStore,
              public validationService: ValidationService,
              public inboxService: InboxService) {
    this.highestValidatedLevel = this.cookieService.getCookie("highestValidatedLevel") ?? "0.0";
  }

  ngOnInit(): void {
    this.inboxService.addMessage({message:
          "Access data for the db_admin are as follows:\n" +
          "Username = m_rott\n" +
          "Password = C9WS2sHyarDjA8dz", isSelected: true});
  }

  validateDbUserLoginTask(stepper: MatStepper, task: number, expectedUser: string) {
    let validationResult = this.localDbUserValidator.validateLoggedInAsUser(5, task, expectedUser);
    this.errorMessage = validationResult.message;
    if (validationResult.isValid) {
      this.errorMessage = "";
      this.highestValidatedLevel = validationResult.level;
      stepper.next();
    }
  }

  validateLevel(stepper: MatStepper): void {

    this.validationService.validateTask(5, 2).subscribe(result => {
      if(!result.isValid)
      {
        this.errorMessage = result.message;
      } else {
        this.errorMessage = "";
        this.highestValidatedLevel = result.level;
        stepper.next();
        let message: Message = {
          message:
              "Your personal access data for the registration window are as follows:\n" +
              "Username = " + this.cookieService.getCookie("uuid") + "\n" +
              "Password = s5HHdC3SKK7q9T",
          isSelected: true
        }
        this.inboxService.addMessage(message);
      }
    });
  }

  updateHighestValidationStep(to: string, stepper: MatStepper) : void {
    if (this.highestValidatedLevel.localeCompare(to) <= 0) {
      this.highestValidatedLevel =  to;
    }
    this.errorMessage = "";
    stepper.next();
  }
}
