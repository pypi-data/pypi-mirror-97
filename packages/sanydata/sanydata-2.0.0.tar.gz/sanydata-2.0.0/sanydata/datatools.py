#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Team : SANY Heavy Energy DataTeam
# @Time    : 2020/8/05 17:37 下午
# @Author  : THao
import os
import grpc
import json
import sqlite3
import pandas as pd
import model_data_message_pb2
import model_data_message_pb2_grpc
import multiprocessing
import asyncio
import traceback
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
query = gql("""
                query{
                turbineAllSqlite(type:""){
                turbineId
                innerTurbineName
                typeId
                typeName
                ratedPower
                etlType
                Pch2A_Acc
                farmId
                pinyinCode
                farmName
                curveId
                isDynamic
                powerCurve
                ownerTurbineName
                ownerId
                ownerEasyName
                ownerName
                farmCode
                projectName
                country
                province
                city
                address
                farmLongitude
                farmLatitude
                capacity
                installedNum
                loopName
                loopOrder
                protocolId
                ratedTorque
                ratedSpeed
                gridSpeed
                cutInSpeed
                cutOutSpeed
                minimumBladeAngle
                hubHeight
                plcIp
                turbineLongitude
                turbineLatitude
                windId
                airDensity
                annualAverageWindSpeed
                turbulenceIntensity
                windShear
                inflowAngle
                windDistributionParameter
                }
                }
                """)
key_map = dict(zip(
    [
        "turbineId",
        "innerTurbineName",
        "typeId",
        "typeName",
        "ratedPower",
        "etlType",
        "Pch2A_Acc",
        "farmId",
        "pinyinCode",
        "farmName",
        "curveId",
        "isDynamic",
        "powerCurve",
        "ownerTurbineName",
        "ownerId",
        "ownerEasyName",
        "ownerName",
        "farmCode",
        "projectName",
        "country",
        "province",
        "city",
        "address",
        "farmLongitude",
        "farmLatitude",
        "capacity",
        "installedNum",
        "loopName",
        "loopOrder",
        "protocolId",
        "ratedTorque",
        "ratedSpeed",
        "gridSpeed",
        "cutInSpeed",
        "cutOutSpeed",
        "minimumBladeAngle",
        "hubHeight",
        "plcIp",
        "turbineLongitude",
        "turbineLatitude",
        "windId",
        "airDensity",
        "annualAverageWindSpeed",
        "turbulenceIntensity",
        "windShear",
        "inflowAngle",
        "windDistributionParameter",
    ],
    [
        "turbine_id",
        "inner_turbine_name",
        "type_id",
        "type_name",
        "rated_power",
        "etl_type",
        "Pch2A_Acc",
        "farm_id",
        "pinyin_code",
        "farm_name",
        "curve_id",
        "is_dynamic",
        "power_curve",
        "owner_turbine_name",
        "owner_id",
        "owner_easy_name",
        "owner_name",
        "farm_code",
        "project_name",
        "country",
        "province",
        "city",
        "address",
        "farm_longitude",
        "farm_latitude",
        "capacity",
        "installed_num",
        "loop_name",
        "loop_order",
        "protocol_id",
        "rated_torque",
        "rated_speed",
        "grid_speed",
        "cut_in_speed",
        "cut_out_speed",
        "minimum_blade_angle",
        "hub_height",
        "plc_ip",
        "turbine_longitude",
        "turbine_latitude",
        "wind_id",
        "air_density",
        "annual_average_wind_speed",
        "turbulence_intensity",
        "wind_shear",
        "inflow_angle",
        "wind_distribution_parameter",
    ]
))
options = [('grpc.max_message_length', 64 * 1024 * 1024), ('grpc.max_receive_message_length', 64 * 1024 * 1024)]


def stub_channel(func):
    def wrapper(self, *args, **kwargs):
        if len(args) > 0:
            stub = args[0]
            if isinstance(stub, str):
                with grpc.insecure_channel(stub, options=options) as channel:
                    stub = model_data_message_pb2_grpc.ModelDataMessageStub(channel)
                    return func(self, stub, *args[1:], **kwargs)
            else:
                return func(self, stub, *args[1:], **kwargs)

        else:
            stub = kwargs['stub']
            if isinstance(stub, str):
                with grpc.insecure_channel(stub, options=options) as channel:
                    stub = model_data_message_pb2_grpc.ModelDataMessageStub(channel)
                    kwargs['stub'] = stub
                    return func(self, **kwargs)
            else:
                return func(self, **kwargs)

    return wrapper


class DataTools(object):
    # This programme is to get data.
    PROGRAMME = 'DataTools'
    VERSION = '2.0.0'

    @staticmethod
    def split_list(list_x, n):
        if n > len(list_x):
            n1 = [1] * len(list_x)
        else:
            a1 = len(list_x) // n
            a2 = len(list_x) % n
            n1 = [a1] * (n - a2) + [a1 + 1] * a2
        res = list()
        s = 0
        for i in n1:
            res.append(list_x[s:s + i])
            s += i
        return res

    # @stub_channel
    # def get_files(self, stub, farm, data_type, start_time, end_time, turbine=None):
    #     """
    #     farm：风场中文拼音名（例如：DBCFC）
    #     data_type：数据类型（history、event、second、fault、qd、）
    #     start_time：数据开始时间（包含）
    #     end_time：数据结束时间（包含）
    #     turbine：机组号（例如：001，必须为三位数），可以省略，省略后将得到所有机组数据
    #     return：匹配到的所有文件列表
    #     """
    #     if isinstance(turbine, str) and len(turbine) != 3:
    #         print('请输入正确机组号')
    #         return
    #
    #     if data_type in ['history', 'fault', 'qd']:
    #         regex = '@@/{}/plc-sync/@@time@@/{}/csv/{}_{}@@.csv'.format(farm, data_type, farm, turbine)
    #     elif data_type == 'event':
    #         regex = '@@/{}/plc-sync/@@time@@/event/csv_full/{}_{}@@.csv'.format(farm, farm, turbine)
    #     elif data_type == 'second':
    #         regex = '@@/{}/@@fjdata@@time@@/@@{}#@@.csv.gz'.format(farm, turbine)
    #     else:
    #         regex = None
    #     if not turbine:
    #         regex = regex.replace('None', '')
    #     # 生成需要获取数据的日期列表
    #     time_list = pd.date_range(start_time, end_time, freq='D')
    #     if data_type == 'second':
    #         time_list = [x.strftime('%Y-%m-%d') for x in time_list]
    #         need_month_list = list(set([x[:7] for x in time_list]))
    #     else:
    #         time_list = [x.strftime('%Y%m%d') for x in time_list]
    #         need_month_list = list(set([x[:6] for x in time_list]))
    #
    #     result_list = list()
    #     for need_month in need_month_list:
    #         get_regex = regex.replace('time', need_month)
    #         dainput = model_data_message_pb2.GetFileListInput(regex=get_regex)
    #         res = stub.GetFileList(dainput, timeout=20000)
    #         result_list = result_list + json.loads(res.output)
    #         if data_type == 'second' and isinstance(turbine, str) and int(turbine) < 99:
    #             try:
    #                 turbine_2 = turbine[1:]
    #                 get_regex_2 = get_regex.replace('/@@{}#'.format(turbine), '/{}#'.format(turbine_2))
    #                 dainput = model_data_message_pb2.GetFileListInput(regex=get_regex_2)
    #                 res = stub.GetFileList(dainput, timeout=20000)
    #                 result_list = result_list + json.loads(res.output)
    #             except Exception as e:
    #                 print(e)
    #                 traceback.print_exc()
    #     if data_type == 'second':
    #         result_list = [x.replace('csv.gz', 'parquet') for x in result_list if x.split('/')[-2] in time_list]
    #     else:
    #         result_list = [x for x in result_list if x.split('/')[-4] in time_list]
    #
    #     return result_list

    @stub_channel
    def get_files(self, stub, farm, data_type, start_time, end_time, turbine=None):
        """
        farm：风场中文拼音名（例如：DBCFC）
        data_type：数据类型（history、event、second、fault、qd、）
        start_time：数据开始时间（包含）, 例如：'2021-03-03'
        end_time：数据结束时间（包含）， 例如：'2021-03-10'
        turbine：机组号,str或list（例如：'001'，必须为三位数,或['001', '002']），可以省略，省略后将得到所有机组数据
        return：匹配到的所有文件列表
        """
        if isinstance(turbine, str) and len(turbine) == 3:
            turbine = json.dumps([turbine])
        elif isinstance(turbine, list):
            for t in turbine:
                if isinstance(t, str) and len(t) != 3:
                    print('请输入正确机组号')
                    return
            turbine = json.dumps(turbine)
        elif turbine is None:
            turbine = turbine
        else:
            print('请输入正确机组号')
            return

        for str_time in [start_time, end_time]:
            if isinstance(str_time, str) and len(str_time) >= 10:
                str_time = str_time[:10] + ' 00:00:00'
                import datetime
                try:
                    _ = datetime.datetime.strptime(str_time, "%Y-%m-%d %H:%M:%S")
                except Exception as e:
                    print(e)
                    print('请检查时间格式，例如：2021-03-03')
                    return
            else:
                print('请检查时间格式，例如：2021-03-03')
                return
        start_time = start_time[:10] + ' 00:00:00'
        end_time = end_time[:10] + ' 23:59:59'
        try:
            dainput = model_data_message_pb2.GetFileListInput(windfarm=farm, turbines=turbine, filetype=data_type,
                                                              start=start_time, end=end_time)
            res = stub.GetFileList(dainput, timeout=20000)
            result_list = json.loads(res.output)
            if data_type == 'second':
                result_list = [x.replace('csv.gz', 'parquet') for x in result_list]
        except Exception as e:
            print(e)
            print('文件列表获取错误')
            result_list = []
        return result_list

    @stub_channel
    def get_csv_data(self, stub, file_list, columns=None):
        import zipfile
        import io
        from io import StringIO
        df_all = list()
        dainput = model_data_message_pb2.GetTargetFileInput(filelist=json.dumps(file_list))
        for i in stub.GetTargetFile(dainput, timeout=20000):
            try:
                f = zipfile.ZipFile(file=io.BytesIO(i.output))
                if len(f.namelist()) > 0:
                    file_name = f.namelist()[0]
                else:
                    continue
                pure_data = f.read(file_name)
                try:
                    df = pd.read_csv(StringIO(pure_data.decode('gbk')))
                except:
                    df = pd.read_csv(StringIO(pure_data.decode('utf-8')))
                if columns:
                    df_all.append(df[columns])
                else:
                    df_all.append(df)
            except Exception as e:
                print(e)
                traceback.print_exc()

        if len(df_all) > 0:
            df_all = pd.concat(df_all)
            df_all = df_all.reset_index(drop=True)
        else:
            df_all = '请检查传入的文件列表'

        return df_all

    @stub_channel
    def get_data(self, stub, file_list, columns=None):
        """
        file_list：所要获取文件列表
        columns：需要的字段，默认加载所有字段
        return：所查询数据合并成的pandas.DataFrmae，在原有的列上增加turbine_num列，用来标识机组号，例：001
        """
        if isinstance(file_list, list) and len(file_list) > 0:
            df_all = list()
            import os
            import zipfile
            import io
            from io import StringIO
            import time
            import uuid
            dainput = model_data_message_pb2.GetTargetFileInput(filelist=json.dumps(file_list))
            if file_list[0].split('.')[-1] == 'parquet':
                df_all_columns = pd.io.excel.ExcelFile('/tmp/14125.xlsx')
                all_name_dict = dict()
                for sheet in df_all_columns.sheet_names[2:]:
                    df_columns = pd.read_excel(df_all_columns, sheet_name=sheet)
                    df_columns_new = df_columns.dropna(subset=['SCADA编号'])  # 去除为空的行
                    df_columns_new = df_columns_new.set_index('SCADA编号', drop=True)  # 调整index
                    name_dict = df_columns_new['中文描述'].T.to_dict()  # 转换为字典
                    all_name_dict.update(name_dict)
                for i in stub.GetTargetFile(dainput, timeout=20000):
                    try:
                        f = zipfile.ZipFile(file=io.BytesIO(i.output))
                        if len(f.namelist()) > 0:
                            file_name = f.namelist()[0]
                        else:
                            continue
                        file_size = f.getinfo(file_name)
                        file_size = file_size.file_size / 1024 / 1024
                        if file_size > 2.8:
                            turbine_num = file_name.split('#')[0]
                            pure_data = f.read(file_name)
                            fio = io.BytesIO(pure_data)
                            time_now = uuid.uuid1()
                            with open('./parquet_file_grpc_temp_{}.parquet'.format(time_now), "wb") as outfile:
                                outfile.write(fio.getbuffer())
                            if columns:
                                c = [k for k, v in all_name_dict.items() if v in columns]
                                c = c + list(set(columns).difference(set(list(all_name_dict.values()))))
                            else:
                                c = columns
                            df = pd.read_parquet('./parquet_file_grpc_temp_{}.parquet'.format(time_now), columns=c)
                            df = df.rename(columns=all_name_dict)
                            turbine_num = turbine_num.zfill(3)
                            df['turbine_num'] = turbine_num
                            os.remove('./parquet_file_grpc_temp_{}.parquet'.format(time_now))
                            df_all.append(df)
                    except Exception as e:
                        print(e)
                        traceback.print_exc()
            else:
                for i in stub.GetTargetFile(dainput, timeout=20000):
                    try:
                        f = zipfile.ZipFile(file=io.BytesIO(i.output))
                        if len(f.namelist()) > 0:
                            file_name = f.namelist()[0]
                        else:
                            continue
                        turbine_num = file_name.split('_')[1]
                        pure_data = f.read(file_name)
                        try:
                            df = pd.read_csv(StringIO(pure_data.decode('gbk')))
                        except:
                            df = pd.read_csv(StringIO(pure_data.decode('utf-8')))
                        df['turbine_num'] = turbine_num
                        if columns:
                            df_all.append(df[columns + ['turbine_num']])
                        else:
                            df_all.append(df)
                    except Exception as e:
                        print(e)
                        traceback.print_exc()
            if len(df_all) > 0:
                df_all = pd.concat(df_all)
                df_all = df_all.reset_index(drop=True)
        else:
            df_all = '请检查传入的文件列表'
        return df_all

    def put_manager_data(self, stub, files, columns, result_list):
        df = self.get_data(stub, files, columns)
        if isinstance(df, pd.DataFrame) and len(df) > 0:
            result_list.append(df)
        else:
            pass

    @stub_channel
    def get_data_process(self, stub, file_list, columns, process=20):
        """
        file_list：所要获取文件列表
        columns：需要的字段，默认加载所有字段
        process：进程数
        return：所查询数据合并成的pandas.DataFrmae，在原有的列上增加turbine_num列，用来标识机组号，例：001
        """
        if len(file_list) < 10:
            result = self.get_data(stub, file_list, columns=columns)
            return result
        manager = multiprocessing.Manager()
        return_list = manager.list()

        if 100 > len(file_list) > 5:
            process = int((len(file_list) / 10) + 0.5)
        elif len(file_list) <= 5:
            process = 1
        else:
            process = process

        p_list = list()
        for files in self.split_list(file_list, process):
            p = multiprocessing.Process(target=self.put_manager_data, args=(stub, files, columns, return_list))
            p_list.append(p)
            p.start()

        for p1 in p_list:
            p1.join()

        result = [x for x in return_list if isinstance(x, pd.DataFrame)]
        if len(result) > 0:
            result = pd.concat(result)
            result = result.reset_index(drop=True)
        else:
            result = None
        return result

    @stub_channel
    def return_result(self, stub, project_name, wind_farm, data_start_time, data_end_time,
                      turbine_type=None, turbine_num=None, status=None, result=None,
                      result_json=None, upload_fig_path=None, upload_log_path=None,
                      upload_file_path=None, local_fig_path=None, local_log_path=None,
                      local_file_path=None, model_version=None, project_id=None, comment=None, description=None):

        """
        project_name：模型英文名，不可省略
        wind_farm：风场拼音缩写，不可省略
        data_start_time：模型中使用的数据期望开始时间，不可省略（方便后续排查问题查询，格式统一为‘%Y-%m-%d %H:%M:%S’）
        data_end_time：模型中使用的数据期望结束时间，不可省略（格式统一为‘%Y-%m-%d %H:%M:%S’）
        turbine_type：机组型号（字符串，例如：‘SE14125’），可省略
        turbine_num：机组号（字符串，例如：001,002），可省略
        status：判断状态，共分为三种：正常、告警、故障（目的是前端显示颜色，分别为无色、黄色、红色），可省略
        result：模型判断结果（例如：0.8、90，不可判断等），可省略
        result_json：模型产生的其他信息，str(dict())格式，例如：
                    str({'real_start_time':'2020-09-11 00:00:01', 'real_end_time':'2020-09-12 00:00:01'})，
                    real_start_time、real_end_time代表数据真实开始于结束时间，不建议省略（主要留作后续给前段产生动态图的json数据），
        upload_fig_path：模型产生图片云端保存位置，可省略
        upload_log_path：模型产生日志云端保存位置，可省略
        upload_file_path：模型其他文件云端保存位置，可省略
        local_fig_path：模型产生的图片本地保存位置，可省略
        local_log_path：模型产生的日志本地保存位置，可省略
        local_file_path：模型产生的其他文件本地保存位置，可省略
        model_version：模型版本号（例如：1.0.0），可省略，(不建议省略)
        project_id：模型id号（例如：10001），可省略(目前可省略，后续统一之后再设置)
        comment：故障类型，例如：偏航振动异常，地形振动异常
        description：故障/正常短描述，位于图片下方
        return：返回为int数字，如果成功，则返回0，如果失败，则返回1
        注意：
        1）模型执行过程将产生的图片、日志、其他文件等暂保存为"本地"位置(这里本地是指执行代码的环境下)，最终通过调用接口，传入相关参数后，
           接口会自动将本地文件传入云端cos，并删除本地文件
        2）模型上传文件统一格式为：fig、log、file/{模型名字，project_name}/{wind_farm,风场名}/**.png、**.log、**.csv、其他；
          （**代表最终文件命名，命名时应尽可能说明机组号、模型所使用数据时间范围等信息，可以对模型每次执行结果进行区分）
        3）模型本地保存统一格式为：/tmp/sanydata_frpc_**.png、sanydata_frpc_**.log、sanydata_frpc_**.csv、其他
          （上述中**代表最终文件命名，命名时应尽可能避免多文件保存到本地时进行覆盖，建议采用当前时间戳）

        """
        import datetime
        import os
        model_end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        model_start_time = os.getenv('ModelStartTime')
        task_id = int(os.getenv('TaskId'))
        if not model_version:
            model_version = os.getenv('ProjectVersion')

        fig_fio = None
        log_fio = None
        file_fio = None
        # 本地图片处理
        if local_fig_path:
            print(local_fig_path)
            with open(local_fig_path, 'rb') as f:
                fig_fio = f.read()
            os.remove(local_fig_path)
        # 本地日志处理
        if local_log_path:
            with open(local_log_path, 'rb') as f:
                log_fio = f.read()
            os.remove(local_log_path)
        # 本地其他文件处理
        if local_file_path:
            with open(local_file_path, 'rb') as f:
                file_fio = f.read()
            os.remove(local_file_path)

        data_input = model_data_message_pb2.ReturnResultInput(projectname=project_name,
                                                              windfarm=wind_farm, turbinetype=turbine_type,
                                                              turbine=turbine_num, description=description,
                                                              DataStartTime=data_start_time, DataEndTime=data_end_time,
                                                              ModeStartTime=model_start_time,
                                                              ModeEndTime=model_end_time,
                                                              projectid=project_id, projectversion=model_version,
                                                              task_id=task_id, comment=comment,
                                                              result=result, resultjson=result_json, status=status,
                                                              uploadfigpath=upload_fig_path,
                                                              uploadlogpath=upload_log_path,
                                                              uploadfilepath=upload_file_path,
                                                              fig=fig_fio, log=log_fio, file=file_fio)
        res = stub.ReturnResult(data_input, timeout=20000)
        return int(json.loads(res.code))

    @stub_channel
    def put_files(self, stub, local_files, upload_files):
        """
           file_type: 文件类型
           local_files：模型产生的文件本地保存位置，list类型 ，例如：['1.png', '2.png']
           upload_files：模型产生的文件云端保存位置，list类型，例如：['test1/1.png', 'test2/2.png']
           注：local_files与upload_files必须一一对应
           return：云端保存的位置
        """
        if isinstance(local_files, list) and isinstance(upload_files, list):
            import os
            file_type = os.getenv('FileType')
            if not file_type:
                file_type = 'cosfig'
            result = list()
            # 本地其他文件处理
            for local_file_path, upload_file_path in zip(local_files, upload_files):
                if not local_file_path:
                    continue
                with open(local_file_path, 'rb') as f:
                    file_fio = f.read()
                os.remove(local_file_path)
                data_input = model_data_message_pb2.PutFileInput(type=file_type, uploadfilepath=upload_file_path, file=file_fio)
                res = stub.PutFile(data_input, timeout=20000)
                if res.msg:
                    result.append('put_file error, error is {}'.format(res.msg))
                else:
                    result.append(res.coskey)

            return result
        else:
            print('请输入正确文件列表')
            return

    # 保存结果三个分析模块的结果文件
    @stub_channel
    def return_report_result(self, stub, project_name, wind_farm, data_start_time, data_end_time,
                             turbine_type=None, turbine_num=None, status=None, result=None,
                             result_json=None, upload_fig_path=None, upload_log_path=None,
                             upload_file_path=None, local_fig_path=None, local_log_path=None,
                             local_file_path=None, Report_version=None, project_id=None):
        """
        将事件分析，发电量分析，健康分析三个模块的结果文件传入COS上(一次只传一个文件)
        project_name：报表英文名，不可省略
        wind_farm：风场拼音缩写，不可省略
        data_start_time：报表中使用的数据开始时间，不可省略（方便后续排查问题查询，格式统一为‘%Y-%m-%d %H:%M:%S’）
        data_end_time：报表中使用的数据结束时间，不可省略（格式统一为‘%Y-%m-%d %H:%M:%S’）
        turbine_type：机组型号（字符串，例如：‘14125’），可省略
        turbine_num：机组号（字符串，例如：01,02），可省略
        status：判断状态，共分为三种：正常、告警、故障（目的是前端显示颜色，分别为无色、黄色、红色）
        result：报表判断结果（例如：0.8、90，不可判断等），可省略
        result_json：报表产生的其他信息，json格式，可省略（主要留作后续给前段产生动态图的json数据）
        upload_fig_path：报表产生图片云端保存位置，可省略
        upload_log_path：报表产生日志云端保存位置，可省略
        upload_file_path：报表其他文件云端保存位置，可省略
        local_fig_paths：报表产生的图片本地保存位置，可省略
        local_log_path：报表产生的日志本地保存位置，可省略
        local_file_path：报表产生的其他文件本地保存位置，可省略
        Report_version：报表版本号（例如：1.0.0），可省略，(不建议省略)
        project_id：报表id号（例如：10001），可省略(目前可省略，后续统一之后再设置)
        return：返回为int数字，如果成果，则返回0，如果失败，则返回1
        注意：
        1）报表执行过程将产生的图片、日志、其他文件等暂保存为本地位置，最终通过调用接口，传入相关参数后，接口会自动将本地文件传入云端，并删除本地文件
        2）报表上传文件统一格式为：fig、log、file/{报表名字，project_name}/{wind_farm,风场名}/**.png、**.log、**.csv、其他；（**代表最终文件命名，命名时应尽可能说明机组号、报表所使用数据时间等信息，可以对报表每次执行结果进行区分）
        3）报表本地保存统一格式为：/tmp/sanydata_frpc_**.png、sanydata_frpc_**.log、sanydata_frpc_**.csv、其他（上述中**代表最终文件命名，命名时应尽可能避免多文件保存到本地时进行覆盖，建议采用当前时间）

        """
        import datetime
        import os

        Report_end_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        Report_start_time = os.getenv('ReportStartTime')
        task_id = int(os.getenv('TaskId'))

        if not Report_version:
            Report_version = os.getenv('ProjectVersion')


        fig_fio = None
        log_fio = None
        file_fio = None

        # 本地图片处理
        if local_fig_path:
            with open(local_fig_path, 'rb') as f:
                fig_fio = f.read()
            os.remove(local_fig_path)
        # 本地日志处理
        if local_log_path:
            with open(local_log_path, 'rb') as f:
                log_fio = f.read()
            os.remove(local_log_path)
        # 本地文件处理
        if local_file_path:
            with open(local_file_path, 'rb') as f:
                file_fio = f.read()
            os.remove(local_file_path)

        data_input = model_data_message_pb2.ReturnReportResultInput(projectname=project_name,
                                                                    windfarm=wind_farm, turbinetype=turbine_type,
                                                                    turbine=turbine_num,
                                                                    DataStartTime=data_start_time,
                                                                    DataEndTime=data_end_time,
                                                                    ModeStartTime=Report_start_time,
                                                                    ModeEndTime=Report_end_time,
                                                                    projectid=project_id, projectversion=Report_version,
                                                                    task_id=task_id,
                                                                    result=result, resultjson=result_json, status=status,
                                                                    uploadfigpath=upload_fig_path,
                                                                    uploadlogpath=upload_log_path,
                                                                    uploadfilepath=upload_file_path,
                                                                    fig=fig_fio, log=log_fio, file=file_fio)

        res = stub.ReturnReportResult(data_input, timeout=20000)
        return json.loads(res.code)

    @stub_channel
    def return_fault_analy(self, stub, fault_detail_df):
        '''
        将故障明细表插入mysql中
        :param fault_detail_df:  故障明细表
        :param farmid:           风场id
        :param farmname:
        :param turbineid:
        :param turbinetype:
        :param faulttype:
        :return:返回为int数字，如果成果，则返回0，如果失败，则返回1
        '''

        from datetime import datetime

        res_l = list()
        for index, row in fault_detail_df.iterrows():
            pinyincode = row['farm']
            turbinename = row['fan']
            statuscode = row['list_code']
            faultdesc = row['list_name']
            faultpart = row['list_partstyle']
            faultstarttime = row['list_stime']
            faultendtime = row['list_etime']
            downtime = row['list_time']
            dentatime = row['list_mt']
            updatetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            farmid = row['farm_id']
            farmname = row['farm_name']
            turbineid = row['turbine_id']
            turbinetype = row['turbine_type']
            faulttype = row['fault_type']

            data_input = model_data_message_pb2.ReturnFaultAnalyInput(farmid=farmid, pinyincode=pinyincode,
                                                                      farmname=farmname,
                                                                      turbineid=turbineid, turbinename=turbinename,
                                                                      turbinetype=turbinetype, statuscode=statuscode,
                                                                      faultdesc=faultdesc, faulttype=faulttype,
                                                                      faultpart=faultpart, faultstarttime=faultstarttime,
                                                                      faultendtime=faultendtime, downtime=downtime,
                                                                      dentatime=dentatime, updatetime=updatetime)
            res = stub.ReturnFaultAnaly(data_input, timeout=20000)
            res_l.append({index: res})
        return res_l

    @stub_channel
    def return_report_result_status(self, stub, page_feature_sta, page_power_sta, taskname, jobname, farmid=None,
                                    farmname=None, reporttype=None, datestring=None, reportargs=None,
                                    analyzingsummary=None, analyzingreports=None, taskid=None, comment=None,
                                    description=None):
        '''
        将页面显示的指标及文件地址插入mysql中
        :param page_feature_sta: 页面显示前9个指标
        :param page_power_sta:   页面显示的关于发电量3个指标
        :param farmid:
        :param farmname:
        :param turbineid:
        :param turbinetype:
        :param faulttype:
        :param analyzingsummary：分析总结html文件
        :param analyzingreports：分析报表json格式，文件与cos地址
        param comment：备用字段
        param description：备用字段
        :return: 返回为int数字，如果成果，则返回0，如果失败，则返回1
        '''

        from datetime import datetime

        taskname = taskname
        jobname = jobname
        farmid = farmid
        farmname = farmname
        reporttype = reporttype
        datestring = datestring
        reportargs = reportargs
        turbinecount = page_feature_sta['风机台数'].iloc[0]
        averageavailability = page_feature_sta['平均可利用率'].iloc[0]
        totalhalttime = page_feature_sta['总停机时长'].iloc[0]
        haltfrequency = page_feature_sta['停机频次'].iloc[0]
        totalhaltcount = page_feature_sta['总停机次数'].iloc[0]
        averagehalttime = page_feature_sta['平均停机时长'].iloc[0]
        totalhaltturbines = page_feature_sta['总停机台数'].iloc[0]
        mtbf = page_feature_sta['平均无故障时间'].iloc[0]
        mttr = page_feature_sta['平均恢复时间'].iloc[0]
        event_completeness = page_feature_sta['事件记录数据完整率'].iloc[0]
        averagespeed = page_power_sta['平均风速'].iloc[0]
        totalpower = page_power_sta['总发电量'].iloc[0]
        cyclepower = page_power_sta['发电量'].iloc[0]
        history_completeness = page_power_sta['5min数据完整率'].iloc[0]
        analyzingsummary = analyzingsummary
        analyzingreports = analyzingreports
        taskid = taskid
        updatedat = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        createdat = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data_input = model_data_message_pb2.ReturnReportResultStatusInput(taskname=taskname, jobname=jobname,
                                                                          farmid=farmid,
                                                                          farmname=farmname, reporttype=reporttype,
                                                                          datestring=datestring,
                                                                          reportargs=reportargs,
                                                                          turbinecount=turbinecount,
                                                                          averageavailability=averageavailability,
                                                                          averagehalttime=averagehalttime,
                                                                          haltfrequency=haltfrequency,
                                                                          totalhaltcount=totalhaltcount,
                                                                          totalhalttime=totalhalttime,
                                                                          totalhaltturbines=totalhaltturbines,
                                                                          mtbf=mtbf, mttr=mttr, averagespeed=averagespeed,
                                                                          totalpower=totalpower, cyclepower=cyclepower,
                                                                          analyzingsummary=analyzingsummary,
                                                                          analyzingreports=analyzingreports,
                                                                          taskid=taskid, createdat=createdat,
                                                                          updatedat=updatedat, eventcom=event_completeness,
                                                                          historycom=history_completeness, comment=comment,
                                                                          description=description)
        res = stub.ReturnReportResultStatus(data_input, timeout=20000)

        return res


class WindFarmInf(object):
    # This programme is to get wind farm information.
    PROGRAMME = 'WindFarmInf'
    VERSION = '1.1.3'

    def __init__(self, sql_file='/tmp/1597716056484sqlite.sqlite',
                 graphql_url="http://192.168.2.4:8080/graphql", use_grapql=False):
        if os.path.exists(sql_file) & ~use_grapql:
            conn = sqlite3.connect(sql_file)
            self.df_wind_farm_turbine = pd.read_sql('select * from wind_farm_turbine', con=conn)
            self.df_turbine_type_powercurve = pd.read_sql('select * from turbine_type_powercurve', con=conn)
            conn.close()
        else:
            transport = RequestsHTTPTransport(url=graphql_url, verify=True, retries=3,)
            client = Client(transport=transport, fetch_schema_from_transport=True)
            result = client.execute(query)
            self.turbineAllSqlite = pd.DataFrame.from_dict(result["turbineAllSqlite"])
            self.turbineAllSqlite = self.turbineAllSqlite.rename(columns=key_map)
            self.df_wind_farm_turbine = self.turbineAllSqlite
            self.df_turbine_type_powercurve = self.turbineAllSqlite

    def get_rated_power_by_turbine(self, farm, turbine_num):
        """
        farm：需要查询的风场，例：'TYSFCA'
        turbine_num：需要查询的机组号，例：'001'
        return：所查询机组的额定功率，例：2500
        """

        df_turbine = self.df_wind_farm_turbine.query('pinyin_code == @farm & inner_turbine_name == @turbine_num')
        if len(df_turbine) == 0:
            result = '数据库表df_wind_farm_turbine中缺少 {}_{} 机组信息'.format(farm, turbine_num)
        else:
            result = df_turbine['rated_power'].unique().tolist()[0]
            if str(result) not in ['nan', 'None']:
                result = float(result)
            else:
                result = '数据库表df_wind_farm_turbine中缺少 {}_{} 机组信息'.format(farm, turbine_num)

        return result

    def get_power_curve_by_turbine(self, farm, turbine_num):
        """
        farm：需要查询的风场，例：'TYSFCA'
        turbine_num：需要查询的机组号，例：'001'
        return：所查询机组的理论功率曲线,返回pandas.DataFrame,columns=['Wind', 'Power']
        """

        df_turbine = self.df_wind_farm_turbine.query('pinyin_code == @farm & inner_turbine_name == @turbine_num')
        if len(df_turbine) == 0:
            result = '数据库表df_wind_farm_turbine中缺少 {}_{} 机组信息'.format(farm, turbine_num)
        else:
            turbine_id = df_turbine['turbine_id'].values[0]
            farm_id = df_turbine['farm_id'].values[0]
            df_power_curve = self.df_turbine_type_powercurve.query('farm_id == @farm_id & turbine_id == @turbine_id')
            if len(df_power_curve) == 0:
                result = '数据库表turbine_type_powercurve中缺少 {}_{} 机组相关id信息'.format(farm, turbine_num)
            else:
                power_curve = df_power_curve['power_curve'].unique().tolist()[0]
                if power_curve:
                    result = dict()
                    wind = list(json.loads(power_curve).keys())
                    wind = [float(x) for x in wind]
                    power = list(json.loads(power_curve).values())
                    power = [float(x) for x in power]
                    while power[-1] == 0:
                        power.pop()
                    wind = wind[:len(power)]
                    result['Wind'] = wind
                    result['Power'] = power
                    result = pd.DataFrame(result)
                else:
                    result = '数据库表turbine_type_powercurve中缺少 {}_{} 机组理论功率曲线信息'.format(farm, turbine_num)

        return result

    def get_types_by_farm(self, farm):
        """
        farm：需要查询的风场，例：'TYSFCA'
        return：所查询风场的机型list
        """

        df_farm = self.df_wind_farm_turbine.query('pinyin_code == @farm')
        if len(df_farm) == 0:
            result = '数据库表df_wind_farm_turbine中缺少 {} 风场信息'.format(farm)
        else:
            farm_id = df_farm['farm_id'].unique().tolist()[0]
            df_turbin_types = self.df_turbine_type_powercurve.query('farm_id == @farm_id')
            if len(df_turbin_types) == 0:
                result = '数据库表turbine_type_powercurve中缺少 {} 风场相关id信息'.format(farm)
            else:
                result = df_turbin_types['type_name'].unique().tolist()
                if str(result) in ['nan', 'None']:
                    result = '数据库表turbine_type_powercurve中缺少 {} 风场相关id信息'.format(farm)

        return result

    def get_turbines_by_farm(self, farm):
        """
        farm：需要查询的风场，例：'TYSFCA'
        return：所查询风场下所有风机号list
        """

        df_farm = self.df_wind_farm_turbine.query('pinyin_code == @farm')
        if len(df_farm) == 0:
            result = '数据库表df_wind_farm_turbine中缺少 {} 风场信息'.format(farm)
        else:
            result = df_farm['inner_turbine_name'].unique().tolist()
            if str(result) in ['nan', 'None']:
                result = '数据库表df_wind_farm_turbine中缺少 {} 风场信息'.format(farm)
            else:
                result.sort()

        return result

    def get_turbines_by_type(self, farm, type_name):
        """
        farm：需要查询的风场，例：'TYSFCA'
        type_name：需要查询的机型，例：'SE8715'
        return：所查询风场与机型下所有风机号list
        """

        df_farm = self.df_wind_farm_turbine.query('pinyin_code == @farm')
        if len(df_farm) == 0:
            result = '数据库表df_wind_farm_turbine中缺少 {} 风场信息'.format(farm)
        else:
            farm_id = df_farm['farm_id'].unique().tolist()[0]
            df_turbin_type = self.df_turbine_type_powercurve.query('farm_id == @farm_id & type_name == @type_name')
            if len(df_turbin_type) == 0:
                result = '数据库表turbine_type_powercurve中缺少 {} 风场相关信息'.format(farm)
            else:
                turbines = df_turbin_type['turbine_id'].unique().tolist()
                result = df_farm.query('turbine_id in @turbines')['inner_turbine_name'].unique().tolist()
                if str(result) in ['nan', 'None']:
                    result = '数据库表turbine_type_powercurve中缺少 {} 风场相关信息'.format(farm)
                else:
                    result.sort()

        return result

    def get_type_by_turbine(self, farm, turbine_num):
        """
        farm：需要查询的风场，例：'TYSFCA'
        turbine_num：需要查询的机组号，例：'001'
        return：所查询机型，例：'SE8715'
        """
        result = '未查询到{}机组信息'.format(turbine_num)
        turbine_types = self.get_types_by_farm(farm)
        if isinstance(turbine_types, str):
            result = turbine_types
        else:
            for turbine_type in turbine_types:
                type_turbines = self.get_turbines_by_type(farm, turbine_type)
                if isinstance(type_turbines, list):
                    if turbine_num in type_turbines:
                        return turbine_type
                    else:
                        continue
                else:
                    result = type_turbines
        return result

    def get_power_curve_by_type(self, farm, type_name):
        """
        farm：需要查询的风场，例：'TYSFCA'
        tb_type：需要查询的机组型号，例：'SE8715'
        return：所查询机型的理论功率曲线,返回pandas.DataFrame,columns=['Wind', 'Power']
        """

        df_farm = self.df_wind_farm_turbine.query('pinyin_code == @farm')
        if len(df_farm) == 0:
            result = '数据库表df_wind_farm_turbine中缺少 {}_{} 型号机组信息'.format(farm, type_name)
        else:
            farm_id = df_farm['farm_id'].values[0]
            df_power_curve = self.df_turbine_type_powercurve.query('farm_id == @farm_id & type_name == @type_name')
            if len(df_power_curve) > 0:
                power_curve = df_power_curve['power_curve'].unique().tolist()[0]
                if power_curve:
                    result = dict()
                    wind = list(json.loads(power_curve).keys())
                    wind = [float(x) for x in wind]
                    power = list(json.loads(power_curve).values())
                    power = [float(x) for x in power]
                    while power[-1] == 0:
                        power.pop()
                    wind = wind[:len(power)]
                    result['Wind'] = wind
                    result['Power'] = power

                    result = pd.DataFrame(result)
                else:
                    result = '数据库表turbine_type_powercurve中缺少 {}_{} 型号机组理论功率曲线信息'.format(farm, type_name)
            else:
                result = '数据库表turbine_type_powercurve中缺少 {}_{} 型号机组相关信息'.format(farm, type_name)

        return result

    def get_chinese_name_by_farm(self, farm):
        """
        farm：需要查询的风场，例：'TYSFCA'
        return：所查询风场的中文名，如果数据库中不存在中文名，则返回字符串'None'
        """

        df_farm = self.df_wind_farm_turbine.query('pinyin_code == @farm')
        if len(df_farm) == 0:
            result = '数据库表df_wind_farm_turbine中缺少 {} 风场信息'.format(farm)
        else:
            result = str(df_farm['farm_name'].unique()[0])
            if str(result) in ['nan', 'None']:
                result = '数据库表df_wind_farm_turbine中缺少 {} 风场信息'.format(farm)

        return result

    def get_py_code_by_farm(self, chinese_name):
        """
        chinese_name：需要查询的风场的中文名，例：'太阳山二期'
        return：所查询风场的拼音缩写，如果数据库中不存在拼音缩写，则返回字符串'None'
        """

        df_farm = self.df_wind_farm_turbine.query('farm_name == @chinese_name')
        if len(df_farm) == 0:
            result = '数据库表df_wind_farm_turbine中缺少 {} 风场信息'.format(chinese_name)
        else:
            result = str(df_farm['pinyin_code'].unique()[0])
            if str(result) in ['nan', 'None']:
                result = '数据库表df_wind_farm_turbine中缺少 {} 风场信息'.format(chinese_name)

        return result

    def get_etl_type_by_farm(self, farm):
        """
        farm：需要查询的风场，例：'TYSFCA'
        return：所查询风场下 {风机号: etl_type}
        """

        df_farm = self.df_wind_farm_turbine.query('pinyin_code == @farm')
        if len(df_farm) == 0:
            type_result = '数据库表df_wind_farm_turbine中缺少 {} 风场信息'.format(farm)
        else:
            result = df_farm['inner_turbine_name'].unique().tolist()
            if str(result) in ['nan', 'None']:
                type_result = '数据库表df_wind_farm_turbine中缺少 {} 风场信息'.format(farm)
            else:
                result.sort()
                type_result = dict([(turbine, df_farm.loc[df_farm['inner_turbine_name'] == turbine]['etl_type'].max())
                                    for turbine in result])

        return type_result

    def get_speed_by_turbine(self, farm, turbine):
        """
        farm: 需要查询的风场，例："TYSFCA"
        turbine: 需要查询的机组号，例："001"
        return：所查询机组的额定转速和并网转速，返回pandas.DataFrame, columns = ['rated_speed', 'grid_speed']
        """

        df_turbine = self.df_wind_farm_turbine.query('pinyin_code == @farm & inner_turbine_name == @turbine')
        if len(df_turbine) == 0:
            result = '数据库表df_wind_farm_turbine中缺少 {}_{} 机组信息'.format(farm, turbine)
        else:
            rated_speed = df_turbine['rated_speed'].unique().tolist()[0]
            grid_speed = df_turbine['grid_speed'].unique().tolist()[0]
            if str(rated_speed) in ['nan', 'None']:
                result = '数据库表df_wind_farm_turbine中缺少 {}_{} 额定转速信息'.format(farm, turbine)
            elif str(grid_speed) in ['nan', 'None']:
                result = '数据库表df_wind_farm_turbine中缺少 {}_{} 并网转速信息'.format(farm, turbine)
            else:
                result = pd.DataFrame([[rated_speed, grid_speed]], columns=['rated_speed', 'grid_speed'])
        return result

    def get_pch2a_acc_by_turbine(self, farm, turbine):
        """
        farm: 需要查询的风场，例“TYSFCA”
        turbine: 需要查询的机组号，例"001"
        return: 所查询机组的X通道加速度信号的传感器位置，返回str,前后/左右，缺失时默认前后
        """

        df_turbine = self.df_wind_farm_turbine.query('pinyin_code == @farm & inner_turbine_name == @turbine')
        if len(df_turbine) == 0:
            result = '数据库表df_wind_farm_turbine中缺少 {}_{} 机组信息'.format(farm, turbine)
        else:
            result = df_turbine['Pch2A_Acc'].unique().tolist()[0]
            if str(result) in ['nan', 'None']:
                result = '前后'
        return result

    def get_farm_id_by_farm(self, farm):
        """
        farm：需要查询的风场，例：'TYSFCB'
        return：所查询风场的风场id
        """

        df_farm = self.df_wind_farm_turbine.query('pinyin_code == @farm')
        if len(df_farm) == 0:
            result = '数据库表df_wind_farm_turbine中缺少 {} 风场信息'.format(farm)
        else:
            result = str(df_farm['farm_id'].unique()[0])
            if str(result) in ['nan', 'None']:
                result = '数据库表df_wind_farm_turbine中缺少 {} 风场信息'.format(farm)
        return result

    def get_turbine_id_by_turbine(self, farm, turbine):
        """
        farm: 需要查询的风场，例“TYSFCA”
        turbine: 需要查询的机组号，例"001"
        return: 所查询机组风机编号
        """

        df_turbine = self.df_wind_farm_turbine.query('pinyin_code == @farm & inner_turbine_name == @turbine')
        if len(df_turbine) == 0:
            result = '数据库表df_wind_farm_turbine中缺少 {}_{} 机组信息'.format(farm, turbine)
        else:
            result = df_turbine['turbine_id'].unique().tolist()[0]
            if str(result) in ['nan', 'None']:
                result = '数据库表df_wind_farm_turbine中缺少 {}_{} 机组信息'.format(farm, turbine)
        return result
