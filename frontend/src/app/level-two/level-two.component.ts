import { Component } from '@angular/core';
import {CookieService} from "../../lib/services/cookie.service";
import {ValidationService} from "../../lib/services/api/validation.service";
import {LocalDbUserValidator} from "../../lib/validator/local-db-user.validator";
import {UserDataStore} from "../../lib/stores/user-data.store";
import {AbstractControl} from "@angular/forms";
import {MatStepper} from "@angular/material/stepper";
import {LevelValidationResult} from "../../lib/models/levelValidationResult";
import {Message} from "../../lib/models/message.interface";
import {InboxService} from "../../lib/services/api/inbox.service";

@Component({
  selector: 'app-level-two',
  templateUrl: './level-two.component.html',
  styleUrls: ['./level-two.component.scss']
})
export class LevelTwoComponent {
  errorMessage: string = "";
  highestValidatedLevel: string = this.cookieService.getCookie("highestValidationLevel") ?? "0.0";
  countProf?: number = undefined;

  constructor(private cookieService: CookieService,
              private validationService: ValidationService,
              public localDbUserValidator: LocalDbUserValidator,
              public userDataStore: UserDataStore,
              public inboxService: InboxService) {

  }

  validateDbUserLoginTask(stepper: MatStepper) {
    let dbUser: string = this.cookieService.getCookie("uuid") ?? "";
    let validationResult = this.localDbUserValidator.validateLoggedInAsUser(2, 2, dbUser);
    this.errorMessage = validationResult.message;
    if (validationResult.isValid) {
      this.updateHighestValidationStep(validationResult.level, stepper);
    }
  }

  updateHighestValidationStep(to: string, stepper: MatStepper) : void {
    if (this.highestValidatedLevel.localeCompare(to) <= 0) {
      this.highestValidatedLevel =  to;
    }
    this.errorMessage = "";
    stepper.next();
  }

  updateHighestValidationStepWithInbox(to: string, stepper: MatStepper) : void {
    this.highestValidatedLevel =  to;
    this.errorMessage = "";
    stepper.next();
    let message: Message = {
      message:
          "A warm welcome!\n" +
          "Your access data for the registration window are as follows:\n" +
          "Username = " + this.cookieService.getCookie("uuid") + "\n" +
          "Password = s5HHdC3SKK7q9T",
      isSelected: true
    }
    this.inboxService.addMessage(message);
  }

  validateCountProfTask(to: string, stepper: MatStepper) {
    if (this.countProf == undefined)
    {
      this.errorMessage += "The input field is empty!";
      return;
    }
    let payload: { [key: string]: any } = {
      answer: this.countProf
    };
    this.validationService.validateTaskWithPayload(2, 3, payload).subscribe(result => {
      if(result.isValid)
      {
        if (this.highestValidatedLevel.localeCompare(to) <= 0) {
          this.highestValidatedLevel =  to;
        }
        this.errorMessage = "";
        stepper.next();
      } else {
        this.errorMessage = result.message;
      }
    });
  }
}
