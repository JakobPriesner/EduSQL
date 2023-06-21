import { Injectable } from '@angular/core';
import {Message} from "../../models/message.interface";
import {AppComponent} from "../../../app/app.component";
import {ReplaySubject} from "rxjs";

@Injectable({
    providedIn: 'root'
})
export class InboxService {
    public messages: Message[] = [];
    public newMessageCount = 0;
    newMessageCountSubject: ReplaySubject<number> = new ReplaySubject<number>(1);

    constructor() {
        // this.messages = [
        //     { message: 'Message 1', isSelected: false },
        //     { message: 'Message 2', isSelected: true },
        //     { message: 'Message 3', isSelected: false }
        // ];
    }

    addMessage(message: Message): void {
        this.messages.push(message);
        this.updateNewMessageCount();
    }

    getMessages(): Message[] {
        return this.messages;
    }

    toggleSelection(index: number): void {
        this.messages[index].isSelected = !this.messages[index].isSelected;
        this.updateNewMessageCount();
    }

    getSelectedMessages(): Message[] {
        return this.messages.filter(message => message.isSelected);
    }

    updateNewMessageCount(): void {
        this.newMessageCount = this.getSelectedMessages().length;
        this.newMessageCountSubject.next(this.newMessageCount);
    }

    clearSelection(): void {
        this.messages.forEach(message => message.isSelected = false);
        this.updateNewMessageCount();
    }
}
