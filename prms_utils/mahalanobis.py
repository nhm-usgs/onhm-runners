import numpy as np

# http://kldavenport.com/mahalanobis-distance-and-outliers/
def mahalanobis_dist(x, y):
    covariance_xy = np.cov(x, y, rowvar=0)
    inv_covariance_xy = np.linalg.inv(covariance_xy)
    xy_mean = np.mean(x), np.mean(y)
    x_diff = np.array([x_i - xy_mean[0] for x_i in x])
    y_diff = np.array([y_i - xy_mean[1] for y_i in y])
    diff_xy = np.transpose([x_diff, y_diff])

    md = []
    for i in xrange(len(diff_xy)):
        md.append(np.sqrt(np.dot(np.dot(np.transpose(diff_xy[i]), inv_covariance_xy), diff_xy[i])))
    return md


# http://kldavenport.com/mahalanobis-distance-and-outliers/
def md_remove_outliers(x, y, adj):
    md = mahalanobis_dist(x, y)
    threshold = np.mean(md) * adj  # adjust 1.5 accordingly
    nx, ny, outliers = [], [], []
    for i in xrange(len(md)):
        if md[i] <= threshold:
            nx.append(x[i])
            ny.append(y[i])
        else:
            outliers.append(i) # position of removed pair
    return np.array(nx), np.array(ny), np.array(outliers)