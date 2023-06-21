import { Component } from '@angular/core';
import {STEPPER_GLOBAL_OPTIONS} from "@angular/cdk/stepper";
import {CookieService} from "../../lib/services/cookie.service";
import {ValidationService} from "../../lib/services/api/validation.service";
import {LocalDbUserValidator} from "../../lib/validator/local-db-user.validator";
import {UserDataStore} from "../../lib/stores/user-data.store";
import {MatStepper} from "@angular/material/stepper";
import {Task} from "../../lib/models/task";

@Component({
  selector: 'app-level-four',
  templateUrl: './level-four.component.html',
  styleUrls: ['./level-four.component.scss'],
  providers: [
    {
      provide: STEPPER_GLOBAL_OPTIONS,
      useValue: {showError: true},
    },
  ]
})
export class LevelFourComponent {


  errorMessage: string = "";
  highestValidatedLevel: string = "0.0";

  constructor(private cookieService: CookieService,
              private validationService: ValidationService,
              public localDbUserValidator: LocalDbUserValidator,
              public userDataStore: UserDataStore) {

  }

  ngOnInit() {

  }


  checkedTasksNames: string[] = [];

  selectLocationsWithLibary(to: string, stepper: MatStepper) : void {
    this.checkedTasks();

    let payload: { [key: string]: any } = {
      answer: this.checkedTasksNames
    };
    this.validationService.validateTaskWithPayload(4, 2, payload).subscribe(result => {
      this.errorMessage = result.message;
      if(result.isValid)
      {
        if (this.highestValidatedLevel.localeCompare(to) <= 0) {
          this.highestValidatedLevel =  to;
        }
        this.errorMessage = "";
        stepper.next();
      }
    });
  }

  task: Task = {
    name: 'Locations',
    completed: false,
    color: 'primary',
    subtasks: [
      {name: 'Fakultaet Angewandte Natur- und Geisteswissenschaften Wirtschaftswissenschaften', completed: false, color: 'primary'},
      {name: 'Fakultaet Angewandte Natur- und Geisteswissenschaften (Raum 7.E.03) Elektrotechnik Maschinenbau', completed: false, color: 'primary'},
      {name: 'Fakultaet Wirtschaftsingenieurwesen (Raum 20.1.71)', completed: false, color: 'primary'},
      {name: 'Fakultaet Architektur und Bauingenieurwesen Kunststofftechnik Vermessung', completed: false, color: 'primary'},
      {name: 'Fakultaet Informatik und Wirtschaftsinformatik Gestaltung', completed: false, color: 'primary'},
    ],
  };

  allComplete: boolean = false;

  updateAllComplete() {
    this.allComplete = this.task.subtasks != null && this.task.subtasks.every(t => t.completed);
  }

  someComplete(): boolean {
    if (this.task.subtasks == null) {
      return false;
    }
    return this.task.subtasks.filter(t => t.completed).length > 0 && !this.allComplete;
  }

  setAll(completed: boolean) {
    this.allComplete = completed;
    if (this.task.subtasks == null) {
      return;
    }
    this.task.subtasks.forEach(t => (t.completed = completed));
  }

  onSuccessfulLogin(stepper: MatStepper) : void {
    this.errorMessage="";
    stepper.next();
  }

  validateDbUserLoginTask(stepper: MatStepper) {
    let validationResult = this.localDbUserValidator.validateLoggedInAsUser(4, 1, 'p_braun');
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

  checkedTasks(){
    // @ts-ignore
    this.checkedTasksNames = this.task.subtasks
        .filter(subtask => subtask.completed)
        .map(subtask => subtask.name);
  }
}
