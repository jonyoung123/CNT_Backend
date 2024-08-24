from lib.config import accessKey, secretKey, region, bucket_name
import matplotlib
import matplotlib.pyplot as plt
import datetime
import numpy as np
import plotly.graph_objects as go
import boto3
from matplotlib.ticker import ScalarFormatter

matplotlib.use('Agg')


class SolveEquation:

    @staticmethod
    def solve_deformation(response, cnt_length):
        s3 = boto3.client('s3', aws_access_key_id=accessKey, aws_secret_access_key=secretKey, region_name=region)
        # create a time series over a range
        t = np.arange(0, 101, 4)
        # create a space (position) series over a range
        x = np.linspace(0, cnt_length, 10)

        final_data = dict()
        # write out the deformation equation
        data_2d = dict()
        for n in range(1, len(response) + 1):
            mode_data = response[f"mode {n}"]
            # Initialize the w array
            w = np.zeros((len(x), len(t)))
            for i in range(len(x)):
                for j in range(len(t)):
                    w[i, j] = (np.sin(n * np.pi * float(t[i]) / cnt_length) * (mode_data['lambda1'] * np.cos(
                        mode_data['theta1'] * float(t[j])) +
                                                                               mode_data['lambda2'] * np.cos(
                                mode_data['theta1'] * float(t[j])) +
                                                                               mode_data['psi1'] * np.sin(
                                mode_data['phi1'] * float(t[j])) +
                                                                               mode_data['psi2'] * np.sin(
                                mode_data['psi2'] * float(t[j]))))
            final_data[f"mode {n}"] = dict()
            final_data[f"mode {n}"]["time"] = t.tolist()
            final_data[f"mode {n}"]["position"] = x.tolist()
            final_data[f"mode {n}"]["deformation"] = w.tolist()

            url_data = SolveEquation.plot_3d(x, t, w, n, s3)
            final_data[f"mode {n}"]["image_url"] = url_data

            data_2d[f"mode {n}"] = SolveEquation.plot_2d(t, n, cnt_length, mode_data, s3)

        return {
            'data_2d': data_2d,
            'data_3d': final_data
        }

    @staticmethod
    def plot_2d(x, n, cnt_length, mode_data, s3):
        timestamp = datetime.datetime.now()
        data = dict()
        w = np.zeros(len(x))
        x_mid = cnt_length / 2
        for i in range(len(x)):
            w[i] = ((np.sin(n * np.pi * x_mid / cnt_length) * (mode_data['lambda1'] * np.cos(
                mode_data['theta1'] * float(x[i])) +
                                                               mode_data['lambda2'] * np.cos(
                        mode_data['theta1'] * float(x[i])) +
                                                               mode_data['psi1'] * np.sin(
                        mode_data['phi1'] * float(x[i])) +
                                                               mode_data['psi2'] * np.sin(
                        mode_data['psi2'] * float(x[i])))))
        data['time'] = x.tolist()
        data['deflection'] = w.tolist()
        # Create a new figure
        plt.figure()

        # Plotting the data
        if n == 1:
            plt.plot(x, w, marker='o', linestyle='-', color='b', label='Data')
        elif n == 2:
            plt.plot(x, w, marker='*', linestyle='-', color='r', label='Data')
        else:
            plt.plot(x, w, marker='o', linestyle='-', color='c', label='Data')

        # Adding titles and labels
        plt.title(f'2D Plot for mode {n}')
        plt.xlabel('Time (t)')
        plt.ylabel('Deflection (w)')

        # Set the y-axis to use scientific notation
        plt.gca().yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
        plt.gca().yaxis.get_offset_text().set_fontsize(12)

        # Adding a legend
        plt.legend()

        # Save the plot as an image
        plt.savefig(f'plot{n}.png', format='png')  # You can change the filename and format as needed

        s3_file_name1 = f'projectCNT/{timestamp}/plot{n}.png'
        try:
            # Upload the file to S3
            s3.upload_file(f'plot{n}.png',
                           bucket_name, s3_file_name1,
                           ExtraArgs={'ContentType': 'image/png', 'ACL': 'public-read'}
                           )

            # generate image url from s3 bucket
            public_url1 = f"https://{bucket_name}.s3.amazonaws.com/{s3_file_name1}"
            print("Public URL1:", public_url1)
            data["image_url"] = public_url1
        except Exception as e:
            print(f"Error ===>>>> {e}")
        # Optionally, you can also display the plot
        # plt.show()
        return data

    @staticmethod
    def plot_3d(x, t, w, n, s3):
        timestamp = datetime.datetime.now()
        # Creating meshgrid for x and t
        url_data = []
        X, T = np.meshgrid(x, t)

        # Create the figure and 3D axis
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Plot the surface
        surf = ax.plot_surface(X, T, w.T, cmap='plasma',
                               edgecolor='none')  # jet, cividis, Greys, plasma, inferno, coolworm, magma

        # Add color bar which maps values to colors
        fig.colorbar(surf)

        # Set labels with increased padding
        ax.set_xlabel('Position (x)', labelpad=20)
        ax.set_ylabel('Time (t)', labelpad=20)
        ax.set_zlabel('Deflection (w)', labelpad=20)

        # Adjust tick label sizes to reduce clutter
        ax.tick_params(axis='x', labelsize=10, pad=20)
        ax.tick_params(axis='y', labelsize=10, pad=20)
        ax.tick_params(axis='z', labelsize=10, pad=20)

        # Use tight layout to avoid clipping
        plt.tight_layout()

        # Set title
        ax.set_title('Surface Plot of Deflection w(x,t) over Time and Position')
        # Set the z-axis to use scientific notation
        ax.zaxis.set_major_formatter(ScalarFormatter(useMathText=True))
        ax.zaxis.get_offset_text().set_fontsize(12)

        # Save the plot as an image file
        plt.savefig(f'deflection_plot{n}.png')
        s3_file_name = f'projectCNT/{timestamp}/deflection_plot{n}.png'
        try:
            # Upload the file to S3
            s3.upload_file(f'deflection_plot{n}.png',
                           bucket_name, s3_file_name,
                           ExtraArgs={'ContentType': 'image/png', 'ACL': 'public-read'}
                           )

            # generate image url from s3 bucket
            public_url = f"https://{bucket_name}.s3.amazonaws.com/{s3_file_name}"
            print("Public URL:", public_url)
            url_data.append(public_url)
        except Exception as e:
            print(f"Error ===>>>> {e}")
        # Create 3D plot
        fig = go.Figure(data=[go.Surface(z=w, x=t, y=x)])
        fig.update_layout(title='3D Plot of w vs x and t', scene=dict(
            xaxis_title='t',
            yaxis_title='x',
            zaxis_title='w'))

        # Save the plot as an image
        fig.write_image(f"3d_plot{n}.png")  # Save as PNG

        s3_file_name1 = f'projectCNT/{timestamp}/3d_plot{n}.png'
        try:
            # Upload the file to S3
            s3.upload_file(f'3d_plot{n}.png',
                           bucket_name, s3_file_name1,
                           ExtraArgs={'ContentType': 'image/png', 'ACL': 'public-read'}
                           )

            # generate image url from s3 bucket
            public_url1 = f"https://{bucket_name}.s3.amazonaws.com/{s3_file_name1}"
            print("Public URL1:", public_url1)
            url_data.append(public_url1)
        except Exception as e:
            print(f"Error ===>>>> {e}")
        return url_data
