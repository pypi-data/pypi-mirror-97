import click


@click.command()
@click.option('-t', '--time', default=30, help='提前发出通知的时间分钟数')
@click.option('-s', '--source', default='schedule.ics', help='要修改的ics文件路径')
def cli(time, source):
    record = []
    records = []
    target = open('./result.ics', 'w')
    with open(source, 'r+') as f:
        lines = f.readlines()
        for index in range(len(lines)):
            if lines[index] == 'BEGIN:VEVENT\n':
                record.append(index)
            if lines[index][:7] == 'SUMMARY':
                record.append(lines[index])
            if lines[index] == 'END:VEVENT\n':
                record.append(index)
                records.append(record)
                record = []
        last_class_name = records[0][1]
        last_class_index = 0
        cnt = 1
        for index_lines in range(records[0][0]):
            target.write(lines[index_lines])
        for index in range(len(records)):
            if records[index][1] == last_class_name:
                cnt += 1
            else:
                if cnt < 3:
                    duration = 'DURATION:PT' + str(cnt * 50) + 'M\n'
                else:
                    duration = 'DURATION:PT' + str(cnt * 50 + 20) + 'M\n'
                for index_lines in range(records[last_class_index][0], records[last_class_index][2]):
                    if lines[index_lines][0:8] != 'DURATION':
                        target.write(lines[index_lines])
                    else:
                        target.write(duration)
                target.write(
                    'BEGIN:VALARM\nTRIGGER:-PT' + str(time) + 'M\nACTION:DISPLAY\nDESCRIPTION:\nEND:VALARM\n')
                target.write('END:VEVENT\n')
                cnt = 1
                last_class_name = records[index][1]
                last_class_index = index
        target.close()
