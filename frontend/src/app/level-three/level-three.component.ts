import {Component} from '@angular/core';
import {CookieService} from "../../lib/services/cookie.service";
import {ValidationService} from "../../lib/services/api/validation.service";
import {STEPPER_GLOBAL_OPTIONS} from "@angular/cdk/stepper";
import {MatStepper} from "@angular/material/stepper";
import {LocalDbUserValidator} from "../../lib/validator/local-db-user.validator";
import {UserDataStore} from "../../lib/stores/user-data.store";
import {Task} from "../../lib/models/task";

@Component({
  selector: 'app-level-three',
  templateUrl: './level-three.component.html',
  styleUrls: ['./level-three.component.scss'],
  providers: [
    {
      provide: STEPPER_GLOBAL_OPTIONS,
      useValue: {showError: true},
    },
  ]
})
export class LevelThreeComponent {

  errorMessage: string = "";
  highestValidatedLevel: string = "0.0";
  dailyBusinessHours: string = "";
  locationLibary: string[] = [];

  constructor(private cookieService: CookieService,
              private validationService: ValidationService,
              public localDbUserValidator: LocalDbUserValidator,
              public userDataStore: UserDataStore) {

  }

  ngOnInit() {

  }



  selectBusinessHours(to: string, stepper: MatStepper, answer: string) : void {
    let payload: { [key: string]: any } = {
      answer: answer
    };
    this.validationService.validateTaskWithPayload(3, 1, payload).subscribe(result => {
      if(result.isValid)
      {
        if (this.highestValidatedLevel.localeCompare(to)) {
          this.highestValidatedLevel =  to;
        }
        this.errorMessage = "";
        stepper.next();
      }
    });
  }

  checkedTasksNames: string[] = [];

  selectLocationsWithLibary(to: string, stepper: MatStepper) : void {
    this.checkedTasks();

    let payload: { [key: string]: any } = {
      answer: this.checkedTasksNames
    };
    this.validationService.validateTaskWithPayload(3, 2, payload).subscribe(result => {
      console.log(result)
      if(result.isValid)
      {
        if (this.highestValidatedLevel.localeCompare(to)) {
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
    let validationResult = this.localDbUserValidator.validateLoggedInAsUser(3, 0, 'p_braun');
    this.errorMessage = validationResult.message;
    if (validationResult.isValid) {
      this.updateHighestValidationStep(validationResult.level, stepper);
    }
  }

  updateHighestValidationStep(to: string, stepper: MatStepper) : void {
    if (this.highestValidatedLevel.localeCompare(to)) {
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
